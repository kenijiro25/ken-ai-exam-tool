import streamlit as st
import requests

st.set_page_config(page_title="P'Ken Exam Generator", layout="wide")
st.title("💡 เครื่องมือสร้างข้อสอบ Conversation โดย พี่เค็น")

context = st.text_area("1. วางบทสนทนาต้นฉบับที่นี่", height=250)
st.divider()
st.subheader("2. เลือกคำที่จะเจาะช่องว่าง (Fill in the blank)")

inputs = []
cols = st.columns(5) 
for i in range(5):
    with cols[i]:
        st.markdown(f"**คำถามข้อที่ {i+1}**")
        word = st.text_input(f"คำที่เลือก", key=f"w_{i}")
        category = st.selectbox(f"วัดเรื่อง", ["Tense", "Vocabulary", "Idiom", "Manner", "Logic"], key=f"c_{i}")
        inputs.append({"word": word, "type": category})

st.divider()

if st.button("🚀 Generate ข้อสอบ", type="primary", use_container_width=True):
    if not context or not any(item['word'] for item in inputs):
        st.warning("กรุณาใส่ข้อมูลให้ครบครับพี่เค็น")
    else:
        WEBHOOK_URL = "https://my-n8n-production-67b5.up.railway.app/webhook/create-exam" 
        payload = {"context": context, "inputs": inputs}
        
        with st.status("🤖 กำลังแกะห่อข้อสอบให้พี่เค็นครับ...", expanded=True) as status:
            try:
                response = requests.post(WEBHOOK_URL, json=payload)
                if response.status_code == 200:
                    raw_data = response.json()
                    
                    # --- สูตรแกะขยะ JSON ออกให้เหลือแต่ตัวหนังสือข้อสอบ ---
                    if isinstance(raw_data, dict):
                        # ถ้า n8n ส่งมาเป็นโครงสร้าง Gemini เราจะหยิบเฉพาะส่วนที่เป็น Text
                        exam_text = raw_data.get('text', list(raw_data.values())[0])
                    else:
                        exam_text = raw_data
                    
                    status.update(label="✅ เสร็จเรียบร้อยครับพี่!", state="complete", expanded=False)
                    st.divider()
                    st.subheader("📝 ผลลัพธ์ข้อสอบ (ก๊อบไปใช้ได้เลย)")
                    
                    # แสดงผลแบบ Markdown เพื่อให้เว้นบรรทัดสวยงาม
                    st.markdown(exam_text)
                    st.balloons()
                else:
                    st.error(f"Error: {response.status_code}")
            except Exception as e:
                st.error(f"Error: {e}")
