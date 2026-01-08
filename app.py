import streamlit as st
import database as data
import candidate_detail

# 初始化数据库（新增这两行）
data.init_database()
data.insert_sample_data()

# 设置页面配置
st.set_page_config(
    page_title="HR简历管理系统",
    page_icon="👥",
    layout="wide"
)

# 初始化session state
if "show_detail" not in st.session_state:
    st.session_state.show_detail = False
if "selected_candidate" not in st.session_state:
    st.session_state.selected_candidate = None

# 如果正在查看详情页
if st.session_state.show_detail:
    candidate_id = st.session_state.selected_candidate
    candidate = data.get_candidate_by_id(candidate_id)
    
    if candidate:
        # 返回按钮
        if st.button("⬅️ 返回列表"):
            st.session_state.show_detail = False
            st.rerun()
        
        # 显示详情
        candidate_detail.show_candidate_detail(candidate)
    else:
        st.error("候选人不存在")
        st.session_state.show_detail = False

else:
    # 页面标题
    st.title("👥 HR简历管理系统")

    # 创建侧边栏菜单
    menu = st.sidebar.selectbox(
        "选择功能",
        ["候选人列表", "添加候选人", "搜索候选人"]
    )

    # ========== 功能1：候选人列表 ==========
    if menu == "候选人列表":
        st.header("📋 候选人列表")
        
        # 获取所有候选人
        candidates = data.get_all_candidates()
        
        # 显示候选人数量
        st.info(f"共有 {len(candidates)} 位候选人")
        
        # 显示每个候选人的信息
        for candidate in candidates:
            col_info, col_btn = st.columns([5, 1])
            
            with col_info:
                with st.expander(f"👤 {candidate['name']} - {candidate['position']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**📞 电话：** {candidate['phone']}")
                        st.write(f"**📧 邮箱：** {candidate['email']}")
                        st.write(f"**💼 工作经验：** {candidate['experience']}")
                    
                    with col2:
                        st.write(f"**🎓 学历：** {candidate['education']}")
                        st.write(f"**📊 状态：** {candidate['status']}")
                        
                        # 显示标签
                        tags_str = "  ".join([f"`{tag}`" for tag in candidate['tags']])
                        st.write(f"**🏷️ 技能标签：** {tags_str}")
            
            with col_btn:
                # 添加"查看详情"按钮
                if st.button("📋 详情", key=f"detail_{candidate['id']}"):
                    st.session_state.selected_candidate = candidate['id']
                    st.session_state.show_detail = True
                    st.rerun()

    # ========== 功能2：添加候选人 ==========
    elif menu == "添加候选人":
        st.header("➕ 添加新候选人")
        
        # 创建表单
        with st.form("add_candidate_form"):
            st.subheader("基本信息")
            
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("姓名 *", placeholder="请输入姓名")
                phone = st.text_input("手机号 *", placeholder="13800138000")
                position = st.text_input("当前职位", placeholder="如：Java工程师")
            
            with col2:
                email = st.text_input("邮箱", placeholder="example@email.com")
                experience = st.selectbox("工作年限", ["1年以内", "1-3年", "3-5年", "5-10年", "10年以上"])
                education = st.selectbox("学历", ["高中", "专科", "本科", "硕士", "博士"])
            
            status = st.selectbox("状态", ["待沟通", "沟通中", "面试中", "已入职", "不合适"])
            
            tags_input = st.text_input("技能标签（用逗号分隔）", placeholder="如：Java,Python,MySQL")
            
            # 提交按钮
            submitted = st.form_submit_button("💾 保存候选人")
            
            if submitted:
                # 验证必填项
                if not name or not phone:
                    st.error("❌ 姓名和手机号为必填项！")
                else:
                    # 处理标签
                    tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
                    
                    # 创建候选人数据
                    new_candidate = {
                        "name": name,
                        "phone": phone,
                        "email": email,
                        "position": position,
                        "experience": experience,
                        "education": education,
                        "status": status,
                        "tags": tags
                    }
                    
                    # 添加到数据库
                    data.add_candidate(new_candidate)
                    
                    st.success(f"✅ 成功添加候选人：{name}")
                    st.balloons()

    # ========== 功能3：搜索候选人 ==========
    elif menu == "搜索候选人":
        st.header("🔍 搜索候选人")
        
        # 搜索框
        keyword = st.text_input("输入姓名搜索", placeholder="请输入候选人姓名")
        
        if st.button("搜索"):
            results = data.search_candidates(keyword)
            
            if results:
                st.success(f"找到 {len(results)} 位候选人")
                
                # 显示搜索结果
                for candidate in results:
                    col_info, col_btn = st.columns([5, 1])
                    
                    with col_info:
                        with st.expander(f"👤 {candidate['name']} - {candidate['position']}"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write(f"**📞 电话：** {candidate['phone']}")
                                st.write(f"**📧 邮箱：** {candidate['email']}")
                                st.write(f"**💼 工作经验：** {candidate['experience']}")
                            
                            with col2:
                                st.write(f"**🎓 学历：** {candidate['education']}")
                                st.write(f"**📊 状态：** {candidate['status']}")
                                tags_str = "  ".join([f"`{tag}`" for tag in candidate['tags']])
                                st.write(f"**🏷️ 技能标签：** {tags_str}")
                    
                    with col_btn:
                        if st.button("📋 详情", key=f"search_detail_{candidate['id']}"):
                            st.session_state.selected_candidate = candidate['id']
                            st.session_state.show_detail = True
                            st.rerun()
            else:
                st.warning("😕 没有找到匹配的候选人")

    # 页脚
    st.sidebar.markdown("---")
    st.sidebar.info("💡 提示：这是一个简单的HR简历管理系统")
