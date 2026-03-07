import streamlit as st

# 1. ตั้งค่าหน้าจอ
st.set_page_config(page_title="P'Ken Prompt Generator", layout="wide")
st.title("💡 เครื่องมือสร้าง Prompt ข้อสอบ โดย พี่เค็น")
st.info("สร้าง Prompt เพื่อให้ AI เจาะช่องว่างบทสนทนาและสรุปหัวข้อวัดเรื่องไว้ตอนท้ายครับ!")

# 2. ส่วนรับบทสนทนาต้นฉบับ
context = st.text_area("1. วางบทสนทนาต้นฉบับที่นี่", height=200, placeholder="วาง Conversation สำหรับทำข้อสอบที่นี่...")

st.divider()

# 3. ส่วนตั้งค่ารายละเอียดข้อสอบ 5 ข้อ
st.subheader("2. ตั้งค่ารายละเอียดข้อสอบ (5 ข้อ)")
inputs = []
cols = st.columns(5) 

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
        ans_key = st.selectbox(f"เฉลยข้อไหน", ["a)", "b)", "c)", "d)"], key=f"a_{i}")
        inputs.append({"word": word, "type": category, "ans": ans_key})

st.divider()

# 4. ปุ่มสร้าง Prompt
if st.button("🚀 สร้าง Prompt สำหรับก๊อบปี้", type="primary", use_container_width=True):
    if not context or not any(item['word'] for item in inputs):
        st.warning("กรุณาใส่บทสนทนาและระบุคำที่จะเจาะช่องว่างก่อนครับพี่เค็น")
    else:
        # ประกอบร่าง Prompt ใหม่ตามเงื่อนไขพี่เค็น
        final_prompt = "จงสร้างข้อสอบภาษาอังกฤษแบบ Multiple Choice (5 ข้อ) โดยใช้บทสนทนาชุดเดียวนี้:\n\n"
        final_prompt += f"--- บทสนทนาต้นฉบับ ---\n{context}\n---------------\n\n"
        final_prompt += "คำสั่งพิเศษจากพี่เค็น:\n"
        final_prompt += "1. ให้แสดง 'บทสนทนาฉบับข้อสอบ' โดยนำคำที่กำหนดด้านล่างนี้ออกจากบทสนทนาเดิม แล้วเปลี่ยนเป็นช่องว่าง '______________' พร้อมใส่หมายเลข (1) - (5) กำกับแทน:\n"
        
        for idx, item in enumerate(inputs):
            if item['word']:
                final_prompt += f"   - เจาะคำว่า [{item['word']}] ออก แล้วเปลี่ยนเป็นช่องว่าง ({idx+1}) ______________\n"
        
        final_prompt += "\n2. สำหรับโจทย์ข้อที่ 1-5 ให้ใช้คำสั่งเดียวกันคือ 'Please use above conversation to choose the best answer' โดยมีเงื่อนไขดังนี้:\n"
        
        for idx, item in enumerate(inputs):
            if item['word']:
                final_prompt += f"   - ข้อที่ {idx+1}: ใช้คำว่า [{item['word']}] เป็นคำตอบที่ถูกต้อง โดยกำหนดให้เป็นตัวเลือกข้อ [{item['ans']}]\n"
        
        final_prompt += "\n3. ห้ามระบุหัวข้อ 'วัดเรื่อง' ในตัวโจทย์แต่ละข้อเด็ดขาด\n"
        final_prompt += "4. ให้สรุปหัวข้อ 'วัดเรื่อง' ของแต่ละข้อไว้ที่ท้ายสุดของข้อสอบหลังส่วนเฉลย โดยใช้หัวข้อดังนี้:\n"
        for idx, item in enumerate(inputs):
            if item['word']:
                final_prompt += f"   - ข้อที่ {idx+1} วัดเรื่อง: {item['type']}\n"
                
        final_prompt += "\n5. ตัวเลือกต้องเป็นแบบ a) b) c) d) และแสดงเฉลยพร้อมคำอธิบายภาษาไทยสไตล์ 'พี่เค็นพาทำ' ให้ละเอียดที่สุด"

        # แสดงผลในกล่อง
        st.subheader("📋 ก๊อบปี้ Prompt นี้ไปแปะใน AI ได้เลยครับพี่!")
        st.text_area("Copy This Prompt:", value=final_prompt, height=500)
        st.success("เรียบร้อยครับ! AI จะเจาะช่องว่างให้พี่เค็น และสรุปเนื้อหาไว้ตอนท้ายตามสั่งครับ")
        st.balloons()
