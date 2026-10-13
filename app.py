import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

st.set_page_config(page_title="하이마트 실적 대시보드", layout="wide")
st.title("📊 하이마트 통합 실적 대시보드")
st.markdown("---")

# 내장형 지점-지사 매핑 사전
hardcoded_mapping = {'NC대전유성': '충청지사', 'NC야탑': '강남지사', '가락': '강남지사', '가야': '부산지사', '간석': '인천지사', '개봉': '강남지사', '거제': '경남제주지사', '건대입구': '강북지사', '검단': '인천지사', '경기광주': '강남지사', '경기광주역': '강남지사', '경북대': '경북지사', '경산': '경북지사', '경암': '호남지사', '경주': '경북지사', '계산': '인천지사', '계양롯데마트': '인천지사', '고덕': '강남지사', '고양롯데마트': '인천지사', '공릉': '강북지사', '공주': '충청지사', '관저': '충청지사', '광교롯데몰': '수원지사', '광명롯데몰': '강남지사', '광복롯데몰': '부산지사', '광산': '호남지사', '광평': '경북지사', '교동': '강원지사', '구로': '강남지사', '구리': '강북지사', '구리역': '강북지사', '구미롯데마트': '경북지사', '군산롯데마트': '호남지사', '금사': '부산지사', '금오': '강북지사', '금천': '강남지사', '금촌': '인천지사', '기장': '부산지사', '김제': '호남지사', '김천': '경북지사', '김포공항롯데마트': '인천지사', '김해내동': '경남제주지사', '나운': '호남지사', '나주': '호남지사', '남양': '수원지사', '남원': '호남지사', '남춘천': '강원지사', '내당': '경북지사', '내서': '경남제주지사', '내포하나로마트': '충청지사', '논산': '충청지사', '논현신도시': '인천지사', '단계': '강원지사', '단구': '강원지사', '당진': '충청지사', '당진롯데마트': '충청지사', '대구율하롯데마트': '경북지사', '대덕롯데마트': '충청지사', '대연': '부산지사', '대잠': '경북지사', '대치': '강남지사', '더나노스퀘어동대문': '강북지사', '덕계': '부산지사', '덕소롯데마트': '강북지사', '덕천': '부산지사', '도계': '경남제주지사', '도동': '경남제주지사', '동광양': '호남지사', '동광주': '호남지사', '동구일산': '부산지사', '동김해': '경남제주지사', '동두천': '강북지사', '동래': '부산지사', '동인천': '인천지사', '동탄호수공원': '수원지사', '동해': '강원지사', '두정': '충청지사', '둔산': '충청지사', '마곡발산': '인천지사', '마리오아울렛': '강남지사', '마산': '경남제주지사', '마석': '강원지사', '만수': '인천지사', '명지': '부산지사', '모란': '강남지사', '목포': '호남지사', '문경': '경북지사', '문경파트너스': '경북지사', '미아사거리': '강북지사', '밀양': '경남제주지사', '발산': '인천지사', '발안': '수원지사', '방축': '충청지사', '범서': '부산지사', '범어네거리': '경북지사', '병': '수원지사', '보령': '충청지사', '복산': '부산지사', '봉담': '수원지사', '봉선': '호남지사', '봉천': '강남지사', '부곡': '부산지사', '부산롯데마트': '부산지사', '부산역': '부산지사', '부여': '충청지사', '부천': '인천지사', '부천중동': '인천지사', '부평구청': '인천지사', '부평롯데마트': '인천지사', '부평역롯데마트': '인천지사', '북변': '인천지사', '북수원': '수원지사', '분당서현': '강남지사', '분평': '충청지사', '비산': '수원지사', '사당': '강남지사', '사상': '부산지사', '사상롯데마트': '부산지사', '사천': '경남제주지사', '사하': '부산지사', '산본': '수원지사', '삼산롯데마트': '인천지사', '삼선교': '강북지사', '삼척': '강원지사', '삼천포': '경남제주지사', '삼화': '경남제주지사', '상계': '강북지사', '상남': '경남제주지사', '상도': '강남지사', '상록수': '수원지사', '상무': '호남지사', '상무롯데마트맥스': '호남지사', '상봉': '강북지사', '상일IC': '강남지사', '상주': '경북지사', '서곡': '호남지사', '서귀포': '경남제주지사', '서대전롯데마트': '충청지사', '서산': '충청지사', '서산롯데마트': '충청지사', '서수원': '수원지사', '서울역롯데마트': '강북지사', '서청주롯데마트': '충청지사', '석관': '강북지사', '석남': '인천지사', '성남시청': '강남지사', '성서': '경북지사', '성정롯데마트': '충청지사', '세종': '충청지사', '센텀': '부산지사', '소사': '인천지사', '소하': '강남지사', '속초': '강원지사', '송도롯데마트': '인천지사', '송우': '강북지사', '송정': '강원지사', '송천': '호남지사', '송탄': '수원지사', '송파롯데마트': '강남지사', '송현': '경북지사', '수송': '호남지사', '수완': '호남지사', '수원': '수원지사', '수지롯데몰': '강남지사', '수진': '강남지사', '시화롯데마트': '수원지사', '시흥롯데마트': '수원지사', '시흥배곧롯데마트': '수원지사', '신길': '강남지사', '신도시고잔': '수원지사', '신방': '충청지사', '신정': '부산지사', '신제주': '경남제주지사', '신천': '수원지사', '쌍문': '강북지사', '쌍용': '충청지사', '아산': '충청지사', '안동옥동': '경북지사', '안산롯데마트': '수원지사', '안산롯데백화': '수원지사', '안산선부': '수원지사', '안산터미널': '수원지사', '안성': '수원지사', '안양': '수원지사', '안중': '수원지사', '압구정': '강남지사', '양산': '부산지사', '양주LF스퀘어': '강북지사', '양평': '강원지사', '언양': '부산지사', '엔터식스안양역': '수원지사', '여수': '호남지사', '여주': '강원지사', '여천': '호남지사', '여천롯데마트': '호남지사', '역곡': '인천지사', '연산': '부산지사', '연수': '인천지사', '연향': '호남지사', '영도': '부산지사', '영등포롯데마트맥스': '강남지사', '영종': '인천지사', '영종도롯데마트': '인천지사', '영주': '경북지사', '영천': '경북지사', '예산': '충청지사', '오광장': '경북지사', '오산': '수원지사', '오정': '인천지사', '오천': '경북지사', '옥정': '강북지사', '옥포': '경남제주지사', '왜관': '경북지사', '용두': '강북지사', '용봉': '호남지사', '용산아이파크몰': '강북지사', '용인': '강남지사', '용인구성': '강남지사', '용전': '충청지사', '우현': '경북지사', '운정': '인천지사', '울산': '부산지사', '울산대': '부산지사', '울산롯데마트': '부산지사', '웅상롯데마트': '부산지사', '원성': '충청지사', '월드컵롯데마트': '호남지사', '월드타워': '강남지사', '월배': '경북지사', '유성': '충청지사', '유천': '충청지사', '율량': '충청지사', '은평': '강북지사', '은평롯데몰': '강북지사', '의왕': '수원지사', '의왕롯데마트': '수원지사', '의정부': '강북지사', '이도': '경남제주지사', '이천': '강원지사', '익산롯데마트': '호남지사', '인동': '경북지사', '인화': '호남지사', '인후': '호남지사', '작전': '인천지사', '잠실': '강남지사', '장량': '경북지사', '장림': '부산지사', '장유': '경남제주지사', '장한평': '강북지사', '전주롯데마트': '호남지사', '정관': '부산지사', '정림': '충청지사', '정왕역': '수원지사', '정읍': '호남지사', '정자': '강남지사', '정자사거리': '수원지사', '제주': '경남제주지사', '제주롯데마트': '경남제주지사', '제천': '강원지사', '조례': '호남지사', '조치원': '충청지사', '주안': '인천지사', '주엽': '인천지사', '죽전': '경북지사', '중계롯데마트': '강북지사', '증평': '충청지사', '지산': '경북지사', '진영': '경남제주지사', '진장롯데마트': '부산지사', '진접': '강원지사', '진주성': '경남제주지사', '진천': '충청지사', '진해': '경남제주지사', '창동': '강북지사', '창원중앙롯데마트맥스': '경남제주지사', '천호역': '강남지사', '철산역': '강남지사', '첨단': '호남지사', '청구': '강북지사', '청라롯데마트': '인천지사', '청량리롯데마트': '강북지사', '청주터미널': '충청지사', '춘천': '강원지사', '춘천롯데마트': '강원지사', '충주롯데마트': '강원지사', '충주연수': '강원지사', '칠곡': '경북지사', '침산': '경북지사', '탄금': '강원지사', '탄현': '인천지사', '태백': '강원지사', '태안': '충청지사', '테크노밸리': '충청지사', '통영': '경남제주지사', '판암': '충청지사', '평내': '강원지사', '평리': '경북지사', '평촌': '수원지사', '평택': '수원지사', '평택고덕': '수원지사', '평택세교': '수원지사', '포천': '강북지사', '풍무': '인천지사', '피트인산본': '수원지사', '하남미사': '강남지사', '하당': '호남지사', '하양': '경북지사', '한샘광교': '수원지사', '한샘분당수지': '강남지사', '한샘센텀': '부산지사', '한샘좌천': '부산지사', '합포': '경남제주지사', '해운대': '부산지사', '행신역': '인천지사', '현풍': '경북지사', '홈씨씨수원': '수원지사', '홈씨씨인천': '인천지사', '홍성': '충청지사', '홍천': '강원지사', '화곡': '인천지사', '화순': '호남지사', '황금': '경북지사', '회룡역': '강북지사', '효문': '부산지사', '효자': '호남지사', '효천': '호남지사'}

target_file = 'BW실적.xlsx'

if not os.path.exists(target_file):
    st.error("⚠️ 서버에 'BW실적.xlsx' 파일이 없습니다. 관리자에게 문의하세요.")
else:
    with st.spinner('실시간 데이터를 불러오고 있습니다...'):
        try:
            df_hiweb = pd.read_excel(target_file, sheet_name="하이웹(렌탈주문관리)")
            df_bw_total = pd.read_excel(target_file, sheet_name="bw(총1)")
            df_bw_net = pd.read_excel(target_file, sheet_name="bw(순2)")
            
            def normalize_name(name):
                if pd.isna(name): return "알수없음"
                name = str(name).strip()
                if name.startswith('H-'): name = name[2:]
                if name.endswith('점'): name = name[:-1]
                if name.endswith('하이마트'): name = name.replace('하이마트', '')
                return name.strip()

            def get_branch_col(df):
                if '접수처명' in df.columns: return '접수처명'
                if 'HR 조직 200' in df.columns: return 'HR 조직 200'
                return df.columns[0]

            for df in [df_hiweb, df_bw_total, df_bw_net]:
                df['정제된매장명'] = df[get_branch_col(df)].apply(normalize_name)
                df['지사명'] = df['정제된매장명'].map(hardcoded_mapping).fillna('기타')

            center_mapping = {
                '강남지사': '1센터(강남)', '강북지사': '2센터(강북)', '수원지사': '3센터(수원)',
                '경북지사': '4센터(경북)', '부산지사': '5센터(부산)', '인천지사': '6센터(인천)',
                '충청지사': '7센터(충청)', '경남제주지사': '8센터(경남제주)', '호남지사': '9센터(호남)',
                '강원지사': '기타(강원)', '기타': '기타(강원)'
            }
            
            for df in [df_hiweb, df_bw_total, df_bw_net]:
                df['센터'] = df['지사명'].map(center_mapping)
                df['구분'] = df['정제된매장명'].apply(lambda x: x if x in ['잠실', '월드타워', '범어네거리'] else '비도급점')
                df['센터분류'] = df.apply(lambda r: r['센터'] if r['구분'] == '비도급점' else r['구분'], axis=1)
                df['지사분류'] = df.apply(lambda r: r['지사명'] if r['구분'] == '비도급점' else r['구분'], axis=1)

            def find_col(df, keywords):
                for kw in keywords:
                    for col in df.columns:
                        if kw in str(col): return col
                return df.columns[-1]

            hiweb_qty = find_col(df_hiweb, ['수량']) 
            tot_qty = find_col(df_bw_total, ['일시불제외', '수량'])
            net_qty = find_col(df_bw_net, ['일시불제외', '수량'])
            hiweb_date = find_col(df_hiweb, ['접수일'])
            tot_date = find_col(df_bw_total, ['SD주문접수일자', '접수일'])
            net_date = find_col(df_bw_net, ['매출확정일', '일자'])

            order_center = ['★ 총계', '[소계] 도급점', '잠실', '월드타워', '범어네거리', '[소계] 비도급점', '1센터(강남)', '2센터(강북)', '3센터(수원)', '4센터(경북)', '5센터(부산)', '6센터(인천)', '7센터(충청)', '8센터(경남제주)', '9센터(호남)', '기타(강원)']
            order_jisa = ['잠실', '월드타워', '범어네거리', '강남지사', '강북지사', '수원지사', '경북지사', '부산지사', '인천지사', '충청지사', '경남제주지사', '호남지사', '강원지사', '기타']
            jisa_only_order = ['강남지사', '강북지사', '수원지사', '경북지사', '부산지사', '인천지사', '충청지사', '경남제주지사', '호남지사', '강원지사', '기타']

            tab1, tab2, tab3, tab4 = st.tabs(["📈 1. 일일실적", "📅 2. 일자별", "🏢 3. 지사별", "📤 4. 실적공유"])
            
            with tab1:
                st.subheader("▶ 하이마트 렌탈 실적현황 (당월 누적)")
                hist_data = {
                    '센터분류': order_center,
                    '25년 평균': [501, 75, 43, 21, 11, 426, 41, 44, 65, 38, 54, 40, 42, 44, 35, 24],
                    '26년 평균': [914, 117, 73, 27, 18, 797, 77, 95, 122, 78, 80, 64, 78, 102, 61, 41],
                    '1월': [689, 104, 64, 23, 17, 585, 68, 61, 93, 40, 72, 32, 58, 69, 61, 31],
                    '2월': [693, 96, 56, 28, 12, 597, 57, 68, 72, 56, 81, 26, 52, 102, 46, 37],
                    '3월': [921, 140, 88, 34, 18, 781, 59, 76, 115, 55, 99, 77, 76, 128, 54, 42],
                    '4월': [955, 127, 73, 35, 19, 828, 73, 121, 112, 59, 71, 82, 79, 138, 58, 35],
                    '5월': [905, 108, 67, 21, 20, 797, 99, 99, 123, 92, 63, 66, 74, 99, 45, 37],
                    '6월': [1097, 125, 80, 27, 18, 972, 106, 127, 149, 114, 73, 79, 94, 111, 73, 46],
                    '7월': [1065, 138, 96, 21, 21, 927, 77, 113, 144, 108, 91, 70, 100, 112, 62, 49],
                    '8월': [1009, 123, 82, 25, 16, 886, 72, 105, 145, 90, 85, 76, 92, 81, 80, 60],
                    '9월': [895, 93, 50, 26, 17, 802, 84, 84, 148, 92, 82, 68, 74, 75, 67, 28],
                    '최근 3개월': [989.7, 118.0, 76.0, 24.0, 18.0, 871.7, 77.7, 100.7, 145.7, 96.7, 86.0, 71.3, 88.7, 89.3, 69.7, 45.7],
                    '당월 목표': [690, 125, 75, 30, 20, 565, 63, 63, 70, 60, 60, 60, 60, 69, 60, 0]
                }
                df_hist = pd.DataFrame(hist_data)
                df_hiweb['DateObj'] = pd.to_datetime(df_hiweb[hiweb_date].astype(str).str.replace('.', '', regex=False), format='%Y%m%d', errors='coerce')
                max_date = df_hiweb['DateObj'].max()
                today_sum = df_hiweb[df_hiweb['DateObj'] == max_date].groupby('센터분류')[hiweb_qty].sum().reset_index(name='당일(DB)')
                db_sum = df_hiweb.groupby('센터분류')[hiweb_qty].sum().reset_index(name='당월 DB')
                tot_sum = df_bw_total.groupby('센터분류')[tot_qty].sum().reset_index(name='당월 총주')
                net_sum = df_bw_net.groupby('센터분류')[net_qty].sum().reset_index(name='당월 순주')
                
                current_df = pd.merge(today_sum, db_sum, on='센터분류', how='outer')
                current_df = pd.merge(current_df, tot_sum, on='센터분류', how='outer')
                current_df = pd.merge(current_df, net_sum, on='센터분류', how='outer').fillna(0)
                dogub = current_df[current_df['센터분류'].isin(['잠실', '월드타워', '범어네거리'])].sum(numeric_only=True)
                dogub['센터분류'] = '[소계] 도급점'
                bidogub = current_df[~current_df['센터분류'].isin(['잠실', '월드타워', '범어네거리'])].sum(numeric_only=True)
                bidogub['센터분류'] = '[소계] 비도급점'
                tot = current_df.sum(numeric_only=True)
                tot['센터분류'] = '★ 총계'
                
                current_df = pd.concat([pd.DataFrame([tot, dogub]), current_df[current_df['센터분류'].isin(['잠실', '월드타워', '범어네거리'])], pd.DataFrame([bidogub]), current_df[~current_df['센터분류'].isin(['잠실', '월드타워', '범어네거리'])]], ignore_index=True)
                final_tab1 = pd.merge(df_hist, current_df, on='센터분류', how='left').fillna(0)
                final_tab1['달성율(DB기준)'] = np.where(final_tab1['당월 목표'] > 0, (final_tab1['당월 DB'] / final_tab1['당월 목표'] * 100).round(1).astype(str) + '%', '-')
                st.dataframe(final_tab1, use_container_width=True, hide_index=True)

            with tab2:
                st.subheader("▶ 지점별 렌탈 수량 (일자별 흐름)")
                target_dates = [(datetime(2026, 9, 29) + timedelta(days=i)).strftime('%m/%d') for i in range(30)]
                def make_pivot(df, date_col, qty_col):
                    df['DateObj'] = pd.to_datetime(df[date_col].astype(str).str.replace('.', '', regex=False), format='%Y%m%d', errors='coerce')
                    df = df.dropna(subset=['DateObj'])
                    df['일자'] = df['DateObj'].dt.strftime('%m/%d')
                    pivot = pd.pivot_table(df, values=qty_col, index='지사분류', columns='일자', aggfunc='sum').fillna(0)
                    pivot['정렬'] = pd.Categorical(pivot.index, categories=order_jisa, ordered=True)
                    pivot = pivot.sort_values('정렬').drop('정렬', axis=1)
                    pivot.loc['[소계] 도급점'] = pivot.loc[['잠실', '월드타워', '범어네거리'], :].sum()
                    pivot.loc['[소계] 비도급점'] = pivot.loc[[c for c in order_jisa[3:] if c in pivot.index], :].sum()
                    pivot.loc['★ 총계'] = pivot.loc['[소계] 도급점'] + pivot.loc['[소계] 비도급점']
                    final_p = pivot.reindex(['★ 총계', '[소계] 도급점', '잠실', '월드타워', '범어네거리', '[소계] 비도급점'] + order_jisa[3:])
                    final_p = final_p.reindex(columns=target_dates, fill_value=0)
                    return final_p.fillna(0).astype(int).astype(str).replace('0', '')
                st.markdown("#### ■ [DB 기준]")
                st.dataframe(make_pivot(df_hiweb.copy(), hiweb_date, hiweb_qty), use_container_width=True)
                st.markdown("#### ■ [총주문 기준]")
                st.dataframe(make_pivot(df_bw_total.copy(), tot_date, tot_qty), use_container_width=True)
                st.markdown("#### ■ [순주문 기준]")
                st.dataframe(make_pivot(df_bw_net.copy(), net_date, net_qty), use_container_width=True)

            with tab3:
                st.subheader("▶ 지사별 실적현황 (세부 매장 단위)")
                branch_db = df_hiweb.groupby(['지사명', '정제된매장명'])[hiweb_qty].sum().reset_index(name='DB')
                branch_tot = df_bw_total.groupby(['지사명', '정제된매장명'])[tot_qty].sum().reset_index(name='총주')
                branch_net = df_bw_net.groupby(['지사명', '정제된매장명'])[net_qty].sum().reset_index(name='순주')
                merged3 = pd.merge(branch_db, branch_tot, on=['지사명', '정제된매장명'], how='outer')
                merged3 = pd.merge(merged3, branch_net, on=['지사명', '정제된매장명'], how='outer').fillna(0)
                merged3[['DB', '총주', '순주']] = merged3[['DB', '총주', '순주']].astype(int)
                merged3 = merged3.rename(columns={'정제된매장명': '지점명'})
                col1, col2 = st.columns(2)
                cols = [col1, col2]
                idx = 0
                for jisa in jisa_only_order:
                    sub_df = merged3[merged3['지사명'] == jisa].copy()
                    if not sub_df.empty:
                        sum_row = pd.DataFrame([{'지사명': jisa, '지점명': f'🔹 [{jisa} 합계]', 'DB': sub_df['DB'].sum(), '총주': sub_df['총주'].sum(), '순주': sub_df['순주'].sum()}])
                        sub_df = pd.concat([sub_df, sum_row], ignore_index=True)
                        with cols[idx % 2]:
                            st.markdown(f"#### 🏢 {jisa}")
                            st.dataframe(sub_df[['지점명', 'DB', '총주', '순주']], use_container_width=True, hide_index=True)
                            st.markdown("<br>", unsafe_allow_html=True)
                        idx += 1

            with tab4:
                st.subheader("▶ 실적 공유 리포트")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("##### 1. 지점별 실적")
                    total_db, total_tot, total_net = df_hiweb[hiweb_qty].sum(), df_bw_total[tot_qty].sum(), df_bw_net[net_qty].sum()
                    t1_total = pd.DataFrame([{'지점': '★합계', '당월 DB': total_db, '총주문': total_tot, '설치완료(순주)': total_net, '시상금(현기준)': f"{total_net*30000:,.0f}"}])
                    t1_data = merged3.copy().rename(columns={'지점명': '지점', 'DB': '당월 DB', '총주': '총주문', '순주': '설치완료(순주)'})
                    t1_data['시상금(현기준)'] = '-'
                    st.dataframe(pd.concat([t1_total, t1_data[['지점', '당월 DB', '총주문', '설치완료(순주)', '시상금(현기준)']].sort_values('설치완료(순주)', ascending=False).head(20)], ignore_index=True), use_container_width=True)

                with col2:
                    st.markdown("##### 2. 팀별 실적 (제품군)")
                    if '제품군 (전사)' in df_bw_net.columns:
                        prod_df = df_bw_net.groupby('제품군 (전사)')[net_qty].sum().reset_index()
                        prod_df.columns = ['구분', '판매건수(건)']
                        prod_df['예상수수료(원, -vat)'] = prod_df['판매건수(건)'] * 210000
                        t2_total = pd.DataFrame([{'구분': '★합계', '판매건수(건)': prod_df['판매건수(건)'].sum(), '예상수수료(원, -vat)': prod_df['예상수수료(원, -vat)'].sum()}])
                        prod_df['예상수수료(원, -vat)'] = prod_df['예상수수료(원, -vat)'].apply(lambda x: f"{x:,.0f}")
                        t2_total['예상수수료(원, -vat)'] = t2_total['예상수수료(원, -vat)'].apply(lambda x: f"{x:,.0f}")
                        st.dataframe(pd.concat([t2_total, prod_df], ignore_index=True), use_container_width=True)
                    else:
                        st.info("BW실적에 제품군 열이 없습니다.")

                col3, col4 = st.columns(2)
                with col3:
                    st.markdown("##### 3. 지사별 실적(도급포함)")
                    t3_df = df_bw_net.groupby('지사명')[net_qty].sum().reset_index()
                    t3_df.columns = ['구분', '판매건수(건)']
                    t3_df['정렬'] = pd.Categorical(t3_df['구분'], categories=jisa_only_order, ordered=True)
                    t3_df = t3_df.sort_values('정렬').drop('정렬', axis=1)
                    t3_df['예상수수료(원, -vat)'] = t3_df['판매건수(건)'] * 210000
                    t3_total = pd.DataFrame([{'구분': '★합계', '판매건수(건)': t3_df['판매건수(건)'].sum(), '예상수수료(원, -vat)': t3_df['예상수수료(원, -vat)'].sum()}])
                    t3_df['예상수수료(원, -vat)'] = t3_df['예상수수료(원, -vat)'].apply(lambda x: f"{x:,.0f}")
                    t3_total['예상수수료(원, -vat)'] = t3_total['예상수수료(원, -vat)'].apply(lambda x: f"{x:,.0f}")
                    st.dataframe(pd.concat([t3_total, t3_df], ignore_index=True), use_container_width=True)

                with col4:
                    st.markdown("##### 4. 지사별 실적(도급제외)")
                    t4_df = df_bw_net[df_bw_net['구분'] == '비도급점'].groupby('지사명')[net_qty].sum().reset_index()
                    t4_df.columns = ['구분', '판매건수(건)']
                    t4_df['정렬'] = pd.Categorical(t4_df['구분'], categories=jisa_only_order, ordered=True)
                    t4_df = t4_df.sort_values('정렬').drop('정렬', axis=1)
                    t4_total = pd.DataFrame([{'구분': '★합계', '판매건수(건)': t4_df['판매건수(건)'].sum()}])
                    for col_name in ['목표 1차', '목표 2차', '목표 3차']:
                        t4_df[col_name], t4_total[col_name] = '', ''
                    st.dataframe(pd.concat([t4_total, t4_df], ignore_index=True), use_container_width=True)

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")