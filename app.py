import streamlit as st

# 1. ตั้งค่าหน้าจอ
st.set_page_config(page_title="P'Ken Prompt Master", layout="wide")

# 2. สร้าง Sidebar สำหรับเลือกเมนู
with st.sidebar:
    st.title("👨‍🏫 พี่เค็นพาทำ")
    st.subheader("เลือกประเภทข้อสอบ")
    menu = st.selectbox(
        "เมนูที่ต้องการ:",
        ["1. Conversation", "2. Tense & Grammar", "3. Reading Comprehension"]
    )
    st.divider()
    st.info("ก๊อบ Prompt ไปใช้ใน ChatGPT/Claude ได้เลยครับพี่!")

# ----------------------------------------------------------------
# เมนูที่ 1: Conversation (ตัวเดิมที่พี่ปรับจูนไว้)
# ----------------------------------------------------------------
if menu == "1. Conversation":
    st.title("💬 เมนูที่ 1: Conversation")
    context = st.text_area("1. วางบทสนทนาต้นฉบับ", height=200)
    
    st.subheader("2. รายละเอียดข้อสอบ (ข้อ 1-5)")
    inputs = []
    cols = st.columns(5)
    categories_conv = ["ความเข้าใจเรื่อง Tense", "การเลือกคำตอบให้เหมาะกับบริบท", "คำศัพท์", "มารยาทในการสนทนา", "การตั้งคำถามให้เหมาะกับบริบท"]
    
    for i in range(5):
        with cols[i]:
            st.markdown(f"**ข้อที่ {i+1}**")
            word = st.text_input(f"คำที่เลือก", key=f"conv_w_{i}")
            cat = st.selectbox(f"วัดเรื่อง", categories_conv, key=f"conv_c_{i}")
            ans = st.selectbox(f"เฉลยข้อไหน", ["a)", "b)", "c)", "d)"], key=f"conv_a_{i}")
            inputs.append({"word": word, "type": cat, "ans": ans})

    if st.button("🚀 สร้าง Prompt Conversation", type="primary", use_container_width=True):
        prompt = f"จงสร้างข้อสอบ Multiple Choice (5 ข้อ) โดยใช้บทสนทนานี้:\n{context}\n\n"
        prompt += "เงื่อนไข:\n1. แสดง 'Exam Passage' เจาะช่องว่าง (1)-(5) ______________\n"
        prompt += "2. ทุกข้อใช้คำถาม 'Please use above conversation'\n"
        for idx, item in enumerate(inputs):
            prompt += f"   - ข้อที่ {idx+1}: คำตอบคือ [{item['word']}] อยู่ในตัวเลือก [{item['ans']}]\n"
        prompt += "3. สรุปท้ายสุดว่าแต่ละข้อวัดเรื่องอะไร (ตามที่กำหนด: " + ", ".join([f"ข้อ {i+1} {v['type']}" for i,v in enumerate(inputs)]) + ")\n"
        prompt += "4. เฉลยและอธิบายภาษาไทยสไตล์ 'พี่เค็นพาทำ'"
        st.text_area("Copy Prompt:", value=prompt, height=400)

# ----------------------------------------------------------------
# เมนูที่ 2: Tense & Grammar (ความยากระดับสอบราชการ)
# ----------------------------------------------------------------
elif menu == "2. Tense & Grammar":
    st.title("✍️ เมนูที่ 2: Tense & Grammar")
    st.info("ข้อสอบชุดนี้จะเป็นข้อที่ 6 - 10 เสมอ (ระดับความยาก: สอบราชการ)")
    
    categories_tense = [
        "Tense", "Tense วัดเรื่อง Passive Voice", "Tense คู่ (เว้น 1 คำ มีบริบทคู่)",
        "Comparison (ขั้นเท่า ขั้นกว่า ขั้นสุด)", "Conjunctions & Connectors",
        "Preposition", "Preposition (เวลา/สถานที่ in on at)", "Relative Pronoun",
        "Relative Pronoun (ตอบ whom แต่ใช้ whose แทน)", "Relative Pronoun (ตอบ that แทน)",
        "If-clause (เว้นกริยาประโยคแรก)", "If-clause (เว้นกริยาประโยคหลัง)",
        "If-clause แบบ If อยู่ตรงกลาง", "Gerund", "Part of Speeches"
    ]
    
    inputs_tense = []
    cols = st.columns(5)
    for i in range(5):
        q_num = i + 6
        with cols[i]:
            st.markdown(f"**ข้อที่ {q_num}**")
            cat = st.selectbox(f"ถามเรื่อง", categories_tense, key=f"tense_c_{i}")
            ans = st.selectbox(f"เฉลยข้อไหน", ["a)", "b)", "c)", "d)"], key=f"tense_a_{i}")
            inputs_tense.append({"num": q_num, "type": cat, "ans": ans})

    if st.button("🚀 สร้าง Prompt Tense & Grammar", type="primary", use_container_width=True):
        prompt = "จงสร้างข้อสอบภาษาอังกฤษแบบ Multiple Choice (a, b, c, d) จำนวน 5 ข้อ\n"
        prompt += "ระดับความยาก: สำหรับสอบเข้ารับราชการ (ก.พ. / ท้องถิ่น)\n"
        prompt += "เงื่อนไขการสร้าง:\n"
        for item in inputs_tense:
            prompt += f"- ข้อที่ {item['num']}: ถามเรื่อง [{item['type']}] โดยให้ข้อที่ถูกต้องคือตัวเลือก [{item['ans']}]\n"
        prompt += "\nการแสดงผล:\n1. เริ่มต้นทุกข้อด้วยคำว่า 'ข้อที่' เสมอ\n"
        prompt += "2. สร้างโจทย์แบบเว้นช่องว่างให้เลือกเติมคำที่ถูกต้อง\n"
        prompt += "3. เฉลยรวมที่เดียวตอนท้ายสุด โดยบอกแค่: ตอบ a) ... b) ... ไม่ต้องอธิบายเยอะ"
        st.text_area("Copy Prompt:", value=prompt, height=400)

# ----------------------------------------------------------------
# เมนูที่ 3: Reading Comprehension
# ----------------------------------------------------------------
elif menu == "3. Reading Comprehension":
    st.title("📖 เมนูที่ 3: Reading Comprehension")
    
    col1, col2 = st.columns(2)
    with col1:
        rtype = st.selectbox("ประเภทบทความ", ["บทความสั้น (Email/ประกาศ)", "บทความยาว (3-4 ย่อหน้า)"])
    with col2:
        topic = st.text_input("หัวข้อที่อยากได้", placeholder="เช่น การจองโรงแรม, ปัญหาสิ่งแวดล้อม")
    
    st.subheader("ตั้งค่าคำถาม (5 ข้อ)")
    start_num = 16 if "สั้น" in rtype else 21
    
    # Checkbox สำหรับเงื่อนไขคำถาม
    c1 = st.checkbox("ข้อที่ 1: ถามชื่อเรื่อง (Title)", value=True)
    c2 = st.checkbox("ข้อที่ 1: ถามวัตถุประสงค์/Main Idea", value=False)
    c3 = st.checkbox("ต้องมีข้อใดข้อหนึ่งถามว่า 'ข้อใดผิด' (Which is FALSE?)", value=True)
    c4 = st.checkbox("ต้องมีข้อใดข้อหนึ่งถามว่า 'ข้อใดถูก' (Which is TRUE?)", value=True)
    c5 = st.checkbox("ต้องมีข้อใดข้อหนึ่งถามความหมายศัพท์ (Synonym/Context)", value=True)
    c6 = st.checkbox("ต้องมีข้อใดข้อหนึ่งถามความหมายของ Pronoun ในบทความ", value=True)
    
    st.divider()
    cols = st.columns(5)
    ans_reading = []
    for i in range(5):
        with cols[i]:
            st.markdown(f"**ข้อที่ {start_num + i}**")
            ans = st.selectbox(f"เฉลย", ["a)", "b)", "c)", "d)"], key=f"read_a_{i}")
            ans_reading.append(ans)

    if st.button("🚀 สร้าง Prompt Reading", type="primary", use_container_width=True):
        prompt = f"จงสร้างบทความ Reading ({rtype}) เกี่ยวกับเรื่อง: {topic}\n"
        if "ยาว" in rtype: prompt += "- ความยาวประมาณ 3-4 ย่อหน้า (ไม่เกินครึ่งหน้า A4)\n"
        
        prompt += f"\nจากนั้นสร้างข้อสอบ 5 ข้อ (เริ่มที่ข้อที่ {start_num} ถึง {start_num+4}) โดยมีเงื่อนไขดังนี้:\n"
        if c1: prompt += f"- ข้อที่ {start_num}: ถามเกี่ยวกับชื่อเรื่อง (Title)\n"
        if c2: prompt += f"- ข้อที่ {start_num}: ถามเกี่ยวกับวัตถุประสงค์หรือ Main Idea\n"
        if c3: prompt += "- มีหนึ่งข้อถามว่า 'ข้อใดผิด' (Which is FALSE?)\n"
        if c4: prompt += "- มีหนึ่งข้อถามว่า 'ข้อใดถูก' (Which is TRUE?)\n"
        if c5: prompt += "- มีหนึ่งข้อถามความหมายคำศัพท์ หรือ Synonym จากเนื้อหา\n"
        if c6: prompt += "- ในบทความต้องมีการใช้ Pronoun และมีหนึ่งข้อถามว่า Pronoun นั้นหมายถึงอะไร\n"
        
        prompt += "\nการเฉลย:\n"
        for i, a in enumerate(ans_reading):
            prompt += f"- ข้อที่ {start_num+i} ตอบตัวเลือก [{a}]\n"
        
        prompt += f"\nหมายเหตุ: เริ่มต้นทุกข้อด้วยคำว่า 'ข้อที่' และเฉลยรวมไว้ท้ายสุดหลังสร้างข้อสอบเสร็จ"
        st.text_area("Copy Prompt:", value=prompt, height=450)
