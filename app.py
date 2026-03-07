import streamlit as st

st.set_page_config(page_title="P'Ken Prompt Generator", layout="wide")
st.title("💡 เครื่องมือสร้าง Prompt ข้อสอบ โดย พี่เค็น")
st.info("ใช้สำหรับสร้างคำสั่ง (Prompt) เพื่อเอาไปแปะใน ChatGPT/Claude ได้ทันที ไม่ต้องง้อ n8n ครับพี่!")

# 1. รับบทสนทนา
context = st.text_area("1. วางบทสนทนาต้นฉบับที่นี่", height=200, placeholder="วาง Conversation ต้นฉบับที่นี่...")

st.divider()

# 2. ส่วนเลือกคำและตำแหน่งเฉลย
st.subheader("2. ตั้งค่ารายละเอียดข้อสอบ (5 ข้อ)")
inputs = []
cols = st.columns(5) 

for i in range(5):
    with cols[i]:
        st.markdown(f"**ข้อที่ {i+1}**")
        word = st.text_input(f"คำที่เลือก", key=f"w_{i}", placeholder="เช่น although")
        category = st.selectbox(f"วัดเรื่อง", ["Tense", "Vocabulary", "Idiom", "Manner", "Logic"], key=f"c_{i}")
        ans_key = st.selectbox(f"เฉลยข้อไหน", ["A", "B", "C", "D"], key=f"a_{i}")
        inputs.append({"word": word, "type": category, "ans": ans_key})

st.divider()

# 3. ส่วนสร้าง Prompt
if st.button("🚀 สร้าง Prompt สำหรับก๊อบปี้", type="primary", use_container_width=True):
    if not context or not any(item['word'] for item in inputs):
        st.warning("กรุณาใส่บทสนทนาและเลือกคำที่ต้องการเจาะช่องว่างด้วยครับพี่เค็น")
    else:
        # เริ่มต้นประกอบร่าง Prompt
        final_prompt = "จงสร้างข้อสอบภาษาอังกฤษแบบ Multiple Choice จากบทสนทนานี้:\n\n"
        final_prompt += f"--- บทสนทนา ---\n{context}\n---------------\n\n"
        final_prompt += "เงื่อนไขการสร้างข้อสอบมีดังนี้:\n"
        
        for idx, item in enumerate(inputs):
            if item['word']:
                final_prompt += f"{idx+1}. ให้นำคำบริเวณ [{item['word']}] มาตั้งเป็นคำถาม โดยวัดเรื่อง [{item['type']}] "
                final_prompt += f"และให้เฉลยข้อที่ถูกต้องอยู่ตัวเลือก [{item['ans']}]\n"
        
        final_prompt += "\nเมื่อสร้างเสร็จแล้ว ให้แสดงเนื้อหาข้อสอบ พร้อมตัวเลือก A, B, C, D และเฉลยพร้อมคำอธิบายภาษาไทยให้พี่เค็นด้วยครับ"

        # แสดงผล Prompt ในกล่องที่ก๊อบปี้ได้ง่าย
        st.subheader("📋 ก๊อบปี้ข้อความข้างล่างนี้ไปแปะใน AI ได้เลยครับพี่!")
        st.text_area("Copy Prompt:", value=final_prompt, height=400)
        st.success("สร้าง Prompt สำเร็จ! พี่เค็นลากคลุมดำก๊อบไปใช้ได้เลยครับ")
        st.balloons()
