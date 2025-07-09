col1, col2, col3 = st.columns([3, 1, 1])
with col2:
    search_query = st.text_input("", placeholder="🔍Rechercher...", label_visibility="collapsed")