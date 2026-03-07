import streamlit as st
import requests

st.set_page_config(page_title="P'Ken Exam Generator", layout="wide")
st.title("💡 เครื่องมือสร้างข้อสอบ โดย พี่เค็น (GPT Edition)")

context = st.text_area("1. วางบทสนทนาต้นฉบับที่นี่", height=250)
st.divider()

st.subheader("2. เลือกคำที่จะเจาะช่องว่าง")
inputs = []
cols = st.columns(5) 
for i in range(5):
    with cols[i]:
        st.markdown(f"**ข้อที่ {i+1}**")
        word = st.text_input(f"คำที่เลือก", key=f"w_{i}")
        category = st.selectbox(f"วัดเรื่อง", ["Tense", "Vocabulary", "Idiom", "Manner", "Logic"], key=f"c_{i}")
        inputs.append({"word": word, "type": category})

st.divider()

if st.button("🚀 Generate ข้อสอบ", type="primary", use_container_width=True):
    if not context or not any(item['word'] for item in inputs):
        st.warning("กรุณาใส่ข้อมูลให้ครบก่อนครับพี่เค็น")
    else:
        WEBHOOK_URL = "https://my-n8n-production-67b5.up.railway.app/webhook/create-exam" 
        payload = {"context": context, "inputs": inputs}
        
        with st.status("🤖 GPT กำลังปั่นข้อสอบให้พี่เค็นครับ...", expanded=True) as status:
            try:
                response = requests.post(WEBHOOK_URL, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    
                    # --- สูตร "หยิบทุกอย่าง" (รองรับ GPT/Gemini/Claude) ---
                    if isinstance(data, dict):
                        # ถ้าเป็น ChatGPT จะอยู่ที่ choices[0].message.content
                        # ถ้าพี่ขี้เกียจแก้ n8n สูตรนี้จะพยายามควานหาเนื้อหาให้เองครับ
                        exam_content = data.get("exam_text", list(data.values())[0])
                    else:
                        exam_content = data

                    status.update(label="✅ ดึงข้อมูลสำเร็จ!", state="complete", expanded=False)
                    st.success("ข้อสอบเจนเสร็จแล้วครับพี่เค็น!")
                    st.info(exam_content) 
                    st.balloons()
                else:
                    st.error(f"Error: n8n ติดขัด (รหัส {response.status_code})")
            except Exception as e:
                st.error(f"เชื่อมต่อไม่ได้: {e}")
