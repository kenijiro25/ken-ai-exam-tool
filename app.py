import streamlit as st

# 1. ตั้งค่าหน้าจอและหัวข้อ
st.set_page_config(page_title="P'Ken Prompt Generator", layout="wide")
st.title("💡 เครื่องมือสร้าง Prompt ข้อสอบ โดย พี่เค็น")
st.info("ใช้สำหรับสร้างคำสั่ง (Prompt) เพื่อเอาไปแปะใน ChatGPT/Claude ได้เลย ไม่ต้องผ่าน n8n ครับพี่!")

# 2. ส่วนรับบทสนทนาต้นฉบับ
context = st.text_area("1. วางบทสนทนาต้นฉบับที่นี่", height=200, placeholder="วาง Conversation สำหรับทำข้อสอบที่นี่...")

st.divider()

# 3. ส่วนตั้งค่ารายละเอียดข้อสอบ 5 ข้อ
st.subheader("2. ตั้งค่ารายละเอียดข้อสอบ (5 ข้อ)")
inputs = []
cols = st.columns(5) 

# รายการ "วัดเรื่อง" แบบใหม่ตามที่พี่เค็นสั่ง
categories = [
    "ความเข้าใจเรื่อง Tense",
    "การเลือกคำตอบให้เหมาะกับบริบท",
    "คำศัพท์",
    "มารยาทในการสนทนา",
    "การตั้งคำถามให้เหมาะกับบริบท"
]

for i in range(5):
    with cols[i]:
        st.markdown(f"**ข้อที่ {i+1}**")
        word = st.text_input(f"คำที่เลือก", key=f"w_{i}", placeholder="เช่น although")
        category = st.selectbox(f"วัดเรื่อง", categories, key=f"c_{i}")
        # ตัวเลือกเฉลยแบบ a) b) c) d)
        ans_key = st.selectbox(f"เฉลยข้อไหน", ["a)", "b)", "c)", "d)"], key=f"a_{i}")
        inputs.append({"word": word, "type": category, "ans": ans_key})

st.divider()

# 4. ปุ่มสร้าง Prompt
if st.button("🚀 สร้าง Prompt สำหรับก๊อบปี้", type="primary", use_container_width=True):
    if not context or not any(item['word'] for item in inputs):
        st.warning("กรุณาใส่บทสนทนาและระบุคำที่ต้องการเจาะช่องว่างก่อนครับพี่เค็น")
    else:
        # ประกอบร่าง Prompt ภาษาไทยแบบที่พี่เค็นต้องการ
        final_prompt = "จงสร้างข้อสอบภาษาอังกฤษแบบ Multiple Choice จากบทสนทนานี้:\n\n"
        final_prompt += f"--- บทสนทนาต้นฉบับ ---\n{context}\n---------------\n\n"
        final_prompt += "เงื่อนไขการสร้างข้อสอบจากพี่เค็น:\n"
        
        count = 1
        for item in inputs:
            if item['word']:
                final_prompt += f"ข้อที่ {count} : ให้นำคำบริเวณ [{item['word']}] มาตั้งเป็นคำถาม โดยวัดเรื่อง [{item['type']}] "
                final_prompt += f"และให้เฉลยข้อที่ถูกต้องอยู่ตัวเลือก [{item['ans']}]\n"
                count += 1
        
        final_prompt += "\nคำแนะนำเพิ่มเติม:\n"
        final_prompt += "- สร้างตัวเลือก 4 ตัวคือ a) b) c) d)\n"
        final_prompt += "- เมื่อสร้างเสร็จแล้ว ให้แสดงเนื้อหาข้อสอบ พร้อมตัวเลือก และเฉลยพร้อมคำอธิบายภาษาไทยให้ละเอียดสไตล์ 'พี่เค็นพาทำ' ด้วยครับ"

        # แสดงผลในกล่อง Text Area ให้ก๊อบง่ายๆ
        st.subheader("📋 ก๊อบปี้ข้อความข้างล่างนี้ไปแปะใน AI ได้เลยครับพี่!")
        st.text_area("Copy This Prompt:", value=final_prompt, height=450)
        st.success("สร้าง Prompt สำเร็จ! พี่เค็นลากคลุมดำก๊อบไปใช้ใน ChatGPT ได้เลยครับ")
        st.balloons()
