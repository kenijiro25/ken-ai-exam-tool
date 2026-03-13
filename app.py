import streamlit as st
import random

# 1. ตั้งค่าหน้าจอ
st.set_page_config(page_title="P'Ken Prompt Master", layout="wide")

# ฟังก์ชันสำหรับ Shuffle เฉลย (แก้ไขใหม่ให้ Work 100%)
def shuffle_answers():
    # ลบ key เก่าออกก่อนเพื่อให้ Widget รีเซ็ตค่าใหม่ตาม random
    keys_to_reset = [k for k in st.session_state.keys() if "ans_key_" in k or "voc_a_" in k]
    for k in keys_to_reset:
        del st.session_state[k]
    
    # สุ่มค่าใหม่ลงไปใน session_state
    for i in range(1, 26): 
        st.session_state[f"ans_key_{i}"] = random.choice(["a)", "b)", "c)", "d)"])
        # สำหรับเมนู Vocab ที่ใช้ key ต่างกันเล็กน้อย
        st.session_state[f"voc_a_{i-11}"] = st.session_state[f"ans_key_{i}"] 

# ฟังก์ชันสำหรับ Clear ค่าทั้งหมด
def clear_all():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# 2. สร้าง Sidebar
with st.sidebar:
    st.title("👨‍🏫 พี่เค็นพาทำ")
    st.subheader("เลือกประเภทข้อสอบ")
    menu = st.selectbox(
        "เมนูที่ต้องการ:",
        [
            "1. Conversation", 
            "2. Tense & Grammar", 
            "3. Vocabulary Mastery", 
            "4. Reading Comprehension"
        ]
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

# --- ส่วนของเมนูอื่นๆ (คงเดิมหรือปรับตาม Logic Shuffle ใหม่) ---
# (ในที่นี้จะขอเจาะจงไปที่เมนู 4 ที่คุณมีปัญหาที่สุดครับ)

if menu == "4. Reading Comprehension":
    st.title("📖 เมนูที่ 4: Reading Comprehension")
    rtype = st.selectbox("ประเภทบทความ", ["บทความสั้น (Email/ประกาศ)", "บทความยาว (3-4 ย่อหน้า)"])
    topic = st.text_input("หัวข้อบทความ", placeholder="ใส่เรื่องที่ต้องการ...")
    start_num = 16 if "สั้น" in rtype else 21
    
    st.subheader("ตั้งค่าคำถาม (ติ๊กข้อไหน AI จะสร้างเฉพาะประเภทนั้น)")
    
    # สร้าง Dict เพื่อเก็บสถานะ
    q_options = {
        "ถามชื่อเรื่อง (Title)": st.checkbox("ถามชื่อเรื่อง (Title)", value=True),
        "ถามวัตถุประสงค์/Main Idea": st.checkbox("ถามวัตถุประสงค์/Main Idea", value=False),
        "ถามว่า 'ข้อใดผิด' (Which is FALSE?)": st.checkbox("ถาม 'ข้อใดผิด' (Which is FALSE?)", value=True),
        "ถามว่า 'ข้อใดถูก' (Which is TRUE?)": st.checkbox("ถาม 'ข้อใดถูก' (Which is TRUE?)", value=True),
        "ถามความหมายของคำศัพท์หรือ Synonym": st.checkbox("ถามศัพท์/Synonym", value=True),
        "ถามว่า Pronoun ในเนื้อหาหมายถึงอะไร": st.checkbox("ถามความหมาย Pronoun", value=True)
    }
    
    # ดึงเฉพาะอันที่ติ๊ก
    questions_logic = [k for k, v in q_options.items() if v]
    
    st.divider()
    cols = st.columns(5)
    ans_reading = []
    for i in range(5):
        q_current = start_num + i
        with cols[i]:
            st.markdown(f"**ข้อที่ {q_current}**")
            # ดึงค่าจาก session_state ที่ถูก shuffle มา
            default_val = st.session_state.get(f"ans_key_{q_current}", "a)")
            ans = st.selectbox(f"ล็อคเฉลย", ["a)", "b)", "c)", "d)"], index=["a)", "b)", "c)", "d)"].index(default_val), key=f"ans_key_{q_current}")
            ans_reading.append({"num": q_current, "key": ans})

    if st.button("🚀 สร้าง Prompt Reading", type="primary", use_container_width=True):
        prompt = f"### [COMMAND: STRICT INSTRUCTIONS]\n"
        prompt += f"1. สร้างบทความภาษาอังกฤษ ({rtype}) เกี่ยวกับเรื่อง: {topic}\n"
        prompt += f"2. สร้างข้อสอบ Multiple Choice จำนวน 5 ข้อ (เลขข้อ {start_num}-{start_num+4})\n\n"
        
        prompt += "### [QUESTION TYPES LIMITATION - สำคัญมาก]\n"
        prompt += "ให้เลือกสร้างคำถาม 'เฉพาะ' ประเภทที่ระบุไว้ในลิสต์ข้างล่างนี้เท่านั้น **ห้ามสร้างประเภทอื่นนอกเหนือจากนี้เด็ดขาด**:\n"
        for logic in questions_logic:
            prompt += f"- {logic}\n"
        
        prompt += "\n### [GENERATE RULES]\n"
        prompt += "- **Chronological Order:** ให้เรียงลำดับคำถามตามเนื้อหาที่ปรากฏในบทความ (ข้อแรกๆ ถามส่วนต้น, ข้อหลังๆ ถามส่วนท้าย)\n"
        prompt += "- **Specific Detail:** ให้ตั้งคำถามเจาะจงที่รายละเอียดเนื้อหา (Fact-based) เพื่อให้ผู้สอบต้องอ่านบทความจริงๆ\n"
        
        prompt += "\n### [ANSWER KEY LOCKING]\n"
        for item in ans_reading:
            prompt += f"- ข้อที่ {item['num']}: กำหนดให้คำตอบที่ถูกต้องคือตัวเลือก [{item['key']}]\n"
        
        prompt += "\n### [FORMATTING]\n"
        prompt += "1. ทุกข้อขึ้นต้นด้วย 'ข้อที่ [เลขข้อ]' เท่านั้น ห้ามระบุชื่อประเภทคำถามในโจทย์\n"
        prompt += "2. แสดงผลเฉลยรวมไว้ท้ายสุด พร้อมสรุปเนื้อความเต็มของข้อที่ถูก และอธิบายเหตุผลสไตล์ 'พี่เค็นพาทำ' เป็นภาษาไทย\n"
        
        st.text_area("Copy Prompt:", value=prompt, height=450)
