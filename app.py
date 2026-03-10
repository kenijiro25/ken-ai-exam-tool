import streamlit as st
import random

# 1. ตั้งค่าหน้าจอ
st.set_page_config(page_title="P'Ken Prompt Master", layout="wide")

# ฟังก์ชันสำหรับ Shuffle เฉลย
def shuffle_answers():
    for i in range(25): # ครอบคลุมทุกเมนู
        st.session_state[f"ans_key_{i}"] = random.choice(["a)", "b)", "c)", "d)"])

# ฟังก์ชันสำหรับ Clear ค่าทั้งหมด
def clear_all():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

# 2. สร้าง Sidebar
with st.sidebar:
    st.title("👨‍🏫 พี่เค็นพาทำ")
    st.subheader("เลือกประเภทข้อสอบ")
    menu = st.selectbox(
        "เมนูที่ต้องการ:",
        ["1. Conversation", "2. Tense & Grammar", "3. Reading Comprehension", "4. Vocabulary Mastery"]
    )
    st.divider()
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        if st.button("🗑️ Clear", use_container_width=True):
            clear_all()
    with col_c2:
        if st.button("🔀 Shuffle", use_container_width=True):
            shuffle_answers()
            st.toast("สุ่มตำแหน่งเฉลยใหม่แล้วครับพี่!")
    st.info("ก๊อบ Prompt ไปใช้ใน ChatGPT/Claude ได้เลยครับพี่!")

# ----------------------------------------------------------------
# เมนูที่ 1: Conversation
# ----------------------------------------------------------------
if menu == "1. Conversation":
    st.title("💬 เมนูที่ 1: Conversation")
    context = st.text_area("1. วางบทสนทนาต้นฉบับ", height=200, key="conv_context")
    
    st.subheader("2. รายละเอียดข้อสอบ (ข้อ 1-5)")
    inputs = []
    cols = st.columns(5)
    categories_conv = ["ความเข้าใจเรื่อง Tense", "การเลือกคำตอบให้เหมาะกับบริบท", "คำศัพท์", "มารยาทในการสนทนา", "การตั้งคำถามให้เหมาะกับบริบท"]
    
    for i in range(5):
        with cols[i]:
            st.markdown(f"**ข้อที่ {i+1}**")
            word = st.text_input(f"คำที่เลือก", key=f"conv_w_{i}")
            cat = st.selectbox(f"วัดเรื่อง", categories_conv, key=f"conv_c_{i}")
            # ใช้ Session State สำหรับ Shuffle
            if f"ans_key_{i}" not in st.session_state:
                st.session_state[f"ans_key_{i}"] = "a)"
            ans = st.selectbox(f"เฉลยข้อไหน", ["a)", "b)", "c)", "d)"], key=f"ans_key_{i}")
            confuse = st.checkbox("ตัวเลือกชวนสับสน", key=f"conv_conf_{i}")
            inputs.append({"word": word, "type": cat, "ans": ans, "confuse": confuse})

    if st.button("🚀 สร้าง Prompt Conversation", type="primary", use_container_width=True):
        prompt = f"จงสร้างข้อสอบ Multiple Choice (5 ข้อ) โดยใช้บทสนทนานี้:\n{context}\n\n"
        prompt += "เงื่อนไขพิเศษจากพี่เค็น:\n"
        prompt += "1. แสดง 'Exam Passage' เจาะช่องว่าง (1)-(5) ______________\n"
        prompt += "2. ทุกข้อใช้คำถาม 'Please use above conversation' เท่านั้น\n"
        
        for idx, item in enumerate(inputs):
            prompt += f"   - ข้อที่ {idx+1}: คำตอบคือ [{item['word']}] ล็อคไว้ที่ตัวเลือก [{item['ans']}]"
            if item['type'] == "มารยาทในการสนทนา":
                prompt += " (เน้นวัดระดับความสุภาพ/Politeness โดยตัวเลือกอื่นต้องมีความหมายคล้ายกันแต่ไม่สุภาพเท่า)"
            if item['confuse']:
                prompt += " **หมายเหตุ: สร้างตัวเลือกหลอกให้มีความใกล้เคียงหรือชวนสับสนที่สุด**"
            prompt += "\n"
            
        prompt += "3. สรุปท้ายสุดว่าแต่ละข้อวัดเรื่องอะไร\n"
        prompt += "4. เฉลยและอธิบายภาษาไทยสไตล์ 'พี่เค็นพาทำ' แสดงเนื้อความเต็มหลังตัวอักษรเฉลย"
        st.text_area("Copy Prompt:", value=prompt, height=400)

# ----------------------------------------------------------------
# เมนูที่ 2: Tense & Grammar
# ----------------------------------------------------------------
elif menu == "2. Tense & Grammar":
    st.title("✍️ เมนูที่ 2: Tense & Grammar")
    st.info("ข้อสอบชุดนี้จะเป็นข้อที่ 6 - 10 เสมอ")
    
    categories_tense = [
        "Tense", "Tense วัดเรื่อง Passive Voice", "Tense คู่ (เว้น 1 คำ มีบริบทคู่)",
        "Comparison (ขั้นเท่า ขั้นกว่า ขั้นสุด)", "Conjunctions & Connectors",
        "Preposition", "Preposition (เวลา/สถานที่ in on at)", "Relative Pronoun",
        "Relative Pronoun (ใช้ whose กรณีที่ข้างหน้าช่องว่างเป็นคน)", 
        "Relative Pronoun (ตอบ that แทน)", "If-clause (เว้นกริยาประโยคแรก)", 
        "If-clause (เว้นกริยาประโยคหลัง)", "If-clause แบบ If อยู่ตรงกลาง", 
        "Gerund", "Part of Speeches"
    ]
    
    inputs_tense = []
    cols = st.columns(5)
    for i in range(5):
        q_num = i + 6
        with cols[i]:
            st.markdown(f"**ข้อที่ {q_num}**")
            cat = st.selectbox(f"ถามเรื่อง", categories_tense, key=f"tense_c_{i}")
            if f"ans_key_{q_num}" not in st.session_state:
                st.session_state[f"ans_key_{q_num}"] = "a)"
            ans = st.selectbox(f"เฉลยข้อไหน", ["a)", "b)", "c)", "d)"], key=f"ans_key_{q_num}")
            inputs_tense.append({"num": q_num, "type": cat, "ans": ans})

    if st.button("🚀 สร้าง Prompt Tense & Grammar", type="primary", use_container_width=True):
        prompt = "จงสร้างข้อสอบภาษาอังกฤษแบบ Multiple Choice (a, b, c, d) ระดับสอบราชการ จำนวน 5 ข้อ\n"
        for item in inputs_tense:
            prompt += f"- ข้อที่ {item['num']}: เรื่อง [{item['type']}] ล็อคเฉลยที่ [{item['ans']}]\n"
        prompt += "เงื่อนไข: เริ่มต้นทุกข้อด้วย 'ข้อที่' และเฉลยรวมท้ายสุดแบบแสดงเนื้อความเต็ม"
        st.text_area("Copy Prompt:", value=prompt, height=400)

# ----------------------------------------------------------------
# เมนูที่ 3: Reading Comprehension
# ----------------------------------------------------------------
elif menu == "3. Reading Comprehension":
    st.title("📖 เมนูที่ 3: Reading Comprehension")
    rtype = st.selectbox("ประเภทบทความ", ["บทความสั้น (Email/ประกาศ)", "บทความยาว (3-4 ย่อหน้า)"])
    topic = st.text_input("หัวข้อบทความ", placeholder="ใส่เรื่องที่ต้องการ...")
    start_num = 16 if "สั้น" in rtype else 21
    
    st.subheader("ตั้งค่าคำถาม")
    c_list = [
        st.checkbox("ถามชื่อเรื่อง (Title)", value=True, key="c1"),
        st.checkbox("ถามวัตถุประสงค์/Main Idea", value=False, key="c2"),
        st.checkbox("ถาม 'ข้อใดผิด' (Which is FALSE?)", value=True, key="c3"),
        st.checkbox("ถาม 'ข้อใดถูก' (Which is TRUE?)", value=True, key="c4"),
        st.checkbox("ถามศัพท์/Synonym", value=True, key="c5"),
        st.checkbox("ถามความหมาย Pronoun", value=True, key="c6")
    ]
    
    cols = st.columns(5)
    ans_reading = []
    for i in range(5):
        q_current = start_num + i
        with cols[i]:
            st.markdown(f"**ข้อที่ {q_current}**")
            if f"ans_key_{q_current}" not in st.session_state:
                st.session_state[f"ans_key_{q_current}"] = "a)"
            ans = st.selectbox(f"ล็อคเฉลย", ["a)", "b)", "c)", "d)"], key=f"ans_key_{q_current}")
            ans_reading.append({"num": q_current, "key": ans})

    if st.button("🚀 สร้าง Prompt Reading", type="primary", use_container_width=True):
        prompt = f"จงสร้างบทความ Reading ({rtype}) เรื่อง: {topic}\n"
        prompt += f"สร้างข้อสอบข้อ {start_num}-{start_num+4} เงื่อนไข: Title/Main Idea, TRUE/FALSE, Synonym, Pronoun Reference\n"
        for item in ans_reading:
            prompt += f"- ข้อที่ {item['num']}: ล็อคเฉลยที่ [{item['key']}]\n"
        prompt += "แสดงเฉลยรวมท้ายสุดพร้อมข้อความเต็มสไตล์ 'พี่เค็นพาทำ'"
        st.text_area("Copy Prompt:", value=prompt, height=400)

# ----------------------------------------------------------------
# เมนูที่ 4: Vocabulary Mastery
# ----------------------------------------------------------------
elif menu == "4. Vocabulary Mastery":
    st.title("🧪 เมนูที่ 4: Vocabulary Mastery")
    inputs_vocab = []
    cols = st.columns(5)
    for i in range(5):
        q_num = i + 11
        with cols[i]:
            st.markdown(f"**ข้อที่ {q_num}**")
            level = st.selectbox(f"ระดับความยาก", ["CEFR B1", "CEFR B2"], key=f"voc_l_{i}")
            if f"ans_key_{q_num}" not in st.session_state:
                st.session_state[f"ans_key_{q_num}"] = "a)"
            ans = st.selectbox(f"เฉลยไว้ที่", ["a)", "b)", "c)", "d)"], key=f"ans_key_{q_num}")
            inputs_vocab.append({"num": q_num, "level": level, "ans": ans})

    if st.button("🚀 สร้าง Prompt Vocabulary", type="primary", use_container_width=True):
        prompt = "จงสร้างข้อสอบคำศัพท์ Oxford 3000 (B1-B2) จำนวน 5 ข้อ (11-15)\n"
        for item in inputs_vocab:
            prompt += f"- ข้อที่ {item['num']}: ระดับ [{item['level']}] ล็อคเฉลยที่ [{item['ans']}]\n"
        prompt += "ห้ามโชว์เลเวลในตัวเลือก, เริ่มต้นทุกข้อด้วย 'ข้อที่', เฉลยรวมท้ายสุดพร้อมข้อความเต็ม"
        st.text_area("Copy Prompt:", value=prompt, height=400)
