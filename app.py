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
cols = st.columns(5) # แบ่งเป็น 5 คอลัมน์สวยๆ

for i in range(5):
    with cols[i]:
        st.markdown(f"**คำถามข้อที่ {i+1}**")
        word = st.text_input(f"คำที่เลือก", key=f"w_{i}", placeholder="เช่น although")
        category = st.selectbox(f"วัดเรื่อง", ["Grammar", "Vocabulary", "Idiom", "Tense", "Logic"], key=f"c_{i}")
        inputs.append({"word": word, "type": category})

st.divider()

# ปุ่ม Generate
if st.button("🚀 Generate ข้อสอบ", type="primary", use_container_width=True):
    if not context or not any(item['word'] for item in inputs):
        st.warning("กรุณาใส่บทสนทนาและเลือกคำอย่างน้อย 1 คำครับพี่เค็น")
    else:
        st.info("กำลังส่งข้อมูลไปให้ Gemini และ Claude วิเคราะห์... (กรุณาต่อ Webhook ใน n8n)")
        # ส่วนนี้เดี๋ยวเรามาต่อ URL Webhook ของ n8n กันครับ
