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
        st.warning("กรุณาใส่ข้อมูลให้ครบก่อนครับพี่เค็น")
    else:
        WEBHOOK_URL = "https://my-n8n-production-67b5.up.railway.app/webhook/create-exam" 
        payload = {"context": context, "inputs": inputs}
        
        with st.status("🤖 กำลังรอ AI หายเหนื่อยและส่งข้อสอบมานะครับ...", expanded=True) as status:
            try:
                response = requests.post(WEBHOOK_URL, json=payload)
                if response.status_code == 200:
                    status.update(label="✅ ดึงข้อมูลสำเร็จ!", state="complete", expanded=False)
                    st.success("ข้อสอบเจนเสร็จแล้วครับพี่เค็น!")
                    st.divider()
                    
                    data = response.json()
                    # แกะห่อหาเนื้อหาข้อสอบ
                    if isinstance(data, dict):
                        exam_content = list(data.values())[0]
                    else:
                        exam_content = data
                    
                    # ถ้าข้อมูลไม่ว่าง ให้โชว์ในกล่องสีฟ้า
                    if exam_content:
                        st.info(exam_content)
                        st.balloons()
                    else:
                        st.warning("AI ไม่ได้ส่งข้อความออกมา (อาจจะโควตาเต็ม) ลองกดใหม่อีกรอบใน 1 นาทีครับพี่")
                else:
                    st.error(f"Error: AI ติดขัด (Status {response.status_code})")
            except Exception as e:
                st.error(f"เชื่อมต่อไม่ได้: {e}")
