import streamlit as st
import requests

st.set_page_config(page_title="P'Ken Exam Generator", layout="wide")

st.title("💡 เครื่องมือสร้างข้อสอบ Conversation โดย พี่เค็น")

# ส่วนบน: ใส่บทสนทนา
context = st.text_area("1. วางบทสนทนาต้นฉบับที่นี่", height=250, placeholder="ใส่ Conversation ที่ต้องการนำมาทำข้อสอบ...")

st.divider()

# ส่วนล่าง: 5 Fields สำหรับ Keywords และ Dropdown
st.subheader("2. เลือกคำที่จะเจาะช่องว่าง (Fill in the blank)")

inputs = []
cols = st.columns(5) 

for i in range(5):
    with cols[i]:
        st.markdown(f"**คำถามข้อที่ {i+1}**")
        word = st.text_input(f"คำที่เลือก", key=f"w_{i}", placeholder="เช่น although")
        category = st.selectbox(f"วัดเรื่อง", ["Tense", "Vocabulary", "Idiom", "Manner", "Logic"], key=f"c_{i}")
        inputs.append({"word": word, "type": category})

st.divider()

# ปุ่ม Generate
if st.button("🚀 Generate ข้อสอบ", type="primary", use_container_width=True):
    if not context or not any(item['word'] for item in inputs):
        st.warning("กรุณาใส่บทสนทนาและเลือกคำอย่างน้อย 1 คำครับพี่เค็น")
    else:
        WEBHOOK_URL = "https://my-n8n-production-67b5.up.railway.app/webhook/create-exam" 
        
        payload = {
            "context": context,
            "inputs": inputs
        }
        
        try:
            # ส่งข้อมูลไปหา n8n
            response = requests.post(WEBHOOK_URL, json=payload)
            if response.status_code == 200:
                st.success("ข้อสอบเจนเสร็จแล้วครับพี่เค็น!")
                st.divider()
                
                # ดึงข้อมูลจาก n8n
                data = response.json()
                
                # ดึงเฉพาะข้อความข้อสอบออกมา (ไม่เอาโค้ด JSON ส่วนเกิน)
                if isinstance(data, dict):
                    # พยายามหาคำว่า exam_text ถ้าไม่มีให้หยิบค่าแรกที่เจอ
                    exam_content = data.get("exam_text", list(data.values())[0])
                else:
                    exam_content = data
                
                # แสดงผลแบบ Markdown เพื่อให้เว้นบรรทัดสวยงาม
                st.markdown(exam_content)
                st.balloons() # ยิงพลุฉลองที่ทำสำเร็จครับพี่!
