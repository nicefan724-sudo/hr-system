import streamlit as st
import database as data


def show_candidate_detail(candidate):
    """显示候选人详情页面"""
    
    st.header(f"👤 {candidate['name']} 的详细信息")
    
    # 创建三列布局
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("工作年限", candidate['experience'])
    with col2:
        st.metric("学历", candidate['education'])
    with col3:
        st.metric("状态", candidate['status'])
    
    st.divider()
    
    # 基本信息
    st.subheader("📋 基本信息")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**📞 电话：** {candidate['phone']}")
        st.write(f"**💼 当前职位：** {candidate['position']}")
    
    with col2:
        st.write(f"**📧 邮箱：** {candidate['email']}")
        tags_str = "  ".join([f"`{tag}`" for tag in candidate['tags']])
        st.write(f"**🏷️ 技能标签：** {tags_str}")
    
    st.divider()
    
    # 简历文件上传
    st.subheader("📤 简历文件")
    
    uploaded_file = st.file_uploader(
        "上传简历文件（PDF/Word/图片）", 
        type=['pdf', 'doc', 'docx', 'jpg', 'png'],
        key=f"file_upload_{candidate['id']}"
    )
    
    if uploaded_file is not None:
        if st.button("💾 保存文件", key=f"save_file_{candidate['id']}"):
            # 保存文件信息
            data.save_uploaded_file(
                candidate['id'], 
                uploaded_file.name, 
                uploaded_file.read()
            )
            st.success(f"✅ 文件 '{uploaded_file.name}' 上传成功！")
    
    # 显示已上传的文件
    files = data.get_candidate_files(candidate['id'])
    if files:
        st.write("**已上传的文件：**")
        for idx, file_info in enumerate(files):
            st.write(f"📄 {idx + 1}. {file_info['name']}")
    else:
        st.info("暂无上传文件")
    
    st.divider()
    
    # 备注/评论功能
    st.subheader("💬 备注与评论")
    
    # 添加新备注
    with st.form(key=f"comment_form_{candidate['id']}"):
        comment_text = st.text_area("添加备注", placeholder="输入对该候选人的评价、面试反馈等...")
        submitted = st.form_submit_button("💬 添加备注")
        
        if submitted and comment_text:
            data.add_comment(candidate['id'], comment_text)
            st.success("✅ 备注已添加")
            st.rerun()  # 刷新页面
    
    # 显示已有备注
    comments = data.get_comments(candidate['id'])
    if comments:
        st.write("**历史备注：**")
        for idx, comment in enumerate(comments, 1):
            with st.container():
                st.markdown(f"""
                <div style="background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                    <small>🕒 {comment['time']}</small><br>
                    {comment['text']}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("暂无备注")
