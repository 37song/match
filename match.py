import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import gspread

# Page configuration
st.set_page_config(page_title="BetterJin309", page_icon="⚽", layout="wide")

# Google Sheets 인증 및 데이터 가져오기
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1uOwA06f9ydm6vbk5dNBX6iiIOjjwNawbdjPBf2dtE98/export?format=csv&gid=680543158"
data = pd.read_csv(spreadsheet_url, header=0)

# Header
st.title("경기 분석")

# Sidebar for user inputs
st.sidebar.header("경기 구성")

# 사이드바 : 종목 선택
sports = ['축구', '농구', '야구']
selected_sport = st.sidebar.selectbox('스포츠 선택', sports)

# 종목 > 리그 목록
league = {
    '축구': ['EPL', 'EFL', '라리가', '분데스리가', '세리에A', '리그1', 'K리그 1', 'K리그 2', 'A리그', '에레디비시에'],
    '농구': ['KBL', 'W-KBL', 'NBA'],
    '야구': ['KBO', 'MLB', 'NPB']
}
# 리그 > 팀 목록
teams_by_league = {
    'EPL': ['A빌라','노팅엄포','뉴캐슬U','레스터C','리버풀','맨체스C','맨체스U','본머스','브라이턴','브렌트퍼','사우샘프','아스널','에버턴','울버햄프','웨스트햄','입스위치','첼시','크리스털','토트넘''풀럼'],
    'EFL': ['브리스C','노리치C','더비카운','루턴타운','리즈U','미들즈브','밀월','번리','브리스C','블랙번','선덜랜드','셰필드U','셰필드웬','스완지C','스토크C','옥스퍼드','왓포드','웨스브로','카디프C','코번트리','퀸즈파크','포츠머스','프레스턴','플리머스''헐시티'],
    '라리가': ['AT마드','RC셀타','라스팔마','라요','레가네스','레알마드','마요르카','바르셀로','바야돌리','발렌시아','베티스','비야레알','빌바오','세비야','소시에다','알라베스','에스파뇰','오사수나','지로나','헤타페'],
    '분데스리가' : ['U베를린','VfL보훔','도르트문','라이프치','레버쿠젠','마인츠05','묀헨글라','바이뮌헨','볼프스부','브레멘','슈투트가','아우크스','장크트파','프라이부','프랑크푸','하이덴하','호펜하임','홀슈타인'],
    '세리에A' : ['AC몬차','AC밀란','AS로마','US레체','나폴리','라치오','베네치아','볼로냐','아탈란타','엘라스','엠폴리','우디네세','유벤투스','인테르','제노아','칼리아리','코모1907','토리노','파르마''피오렌티'],
    '리그1' : ['AS모나코','OGC니스','PSG','RC스트라','낭트','랑스','랭스','르아브르','리옹','릴OSC','마르세유','몽펠리에','브레스투','생테티엔','스타드렌','앙제SCO','오세르','툴루즈'],
    'K리그 1' : ['FC서울','강원FC','광주FC','김천상무','대구FC','대전하나','수원FC','울산HD','인천유나','전북현대','제주유나','포항스틸'],
    'K리그 2' : ['FC안양','경남FC','김포FC','부산아이','부천FC','서울이랜','성남FC','수원삼성','안산그리','전남드래','천안시티','충남아산','충북청주'],
    'A리그' : ['뉴캐제츠','맥아서FC','멜버빅토','멜버시티','브리로어','센트매리','시드니FC','애들유나','오클FC','웨스원더','웨스유나','웰링피닉','퍼스글로'],
    '에레디비시에' : ['F시타르','PSV','고어헤드','네이메헌','발베이크','브레다','빌럼II','스파로테','아약스','알메러C','알크마르','위트레흐','즈볼러','트벤테','페예노르','헤라클레','헤이렌베','흐로닝언'],

    'NBA' : ['LA 레이커스','LA 클리퍼스','골든스테이트','뉴올리언즈','뉴욕','댈러스','덴버','디트로이트','마이애미','멤피스','미네소타','밀워키','보스턴','브루클린','새크라맨토','샌안토니오','샬럿','시카고','애틀랜타','오클라호마','올랜도','워싱턴','유타','인디애나','클리블랜드','토론토','포틀랜드','피닉스','필라델피아','휴스턴'],
    'KBL' : ['KT 소닉붐','고양 캐롯','부산 KCC','서울 SK','서울 삼성','안양 KGC','울산 현대모비스','원주 DB','창원 LG','한국 가스'],
    'W-KBL' : ['BNK썸','KB스타즈','삼성생명','신한은행','우리은행','하나은행'],

    'MLB' : ['LA 다저스','LA 에인절스','뉴욕 메츠','뉴욕 양키스','디트로이트','마이애미','미네소타','밀워키','보스턴','볼티모어','샌디에고','샌프란시스코','세인트루이스','시애틀','시카고 컵스','시카고 화이트삭스','신시네티','애리조나','애틀랜타','오클랜드','워싱턴','캔자스시티','콜로라도','클리블랜드','텍사스','템파베이','토론토','피츠버그','필라델피아','휴스턴'],
    'KBO' : ['KIA','KT','LG','NC','SSG','두산','롯데','삼성','키움','한화'],
    'NPB' : ['니혼햄','라쿠텐','세이부','야쿠르트','오릭스','요미우리','요코하마','주니치','지바 롯데','한신','히로시마']
}

# 팀 선택해서 통계 추출
if selected_sport:
    selected_league = st.sidebar.selectbox("리그 선택", league[selected_sport])
    
    # 리그 변경 감지 및 팀 초기화
    if 'previous_league' not in st.session_state or st.session_state['previous_league'] != selected_league:
        st.session_state['home_team'] = teams_by_league[selected_league][0]
        st.session_state['away_team'] = teams_by_league[selected_league][1]
        st.session_state['previous_league'] = selected_league  # 현재 리그 저장

    st.write(f"By BetterJin309")

    # 팀 선택
    if selected_league in teams_by_league:
        # 홈팀 선택
        home_team = st.sidebar.selectbox(
            "Home Team", 
            teams_by_league[selected_league], 
            index=teams_by_league[selected_league].index(st.session_state['home_team'])
        )
        st.session_state['home_team'] = home_team  # 선택된 홈팀 저장

        # 어웨이 팀 선택 (홈팀과 중복되지 않도록 설정)
        available_away_teams = [team for team in teams_by_league[selected_league] if team != home_team]
        away_team = st.sidebar.selectbox(
            "Away Team",
            available_away_teams,
            index=available_away_teams.index(st.session_state['away_team']) if st.session_state['away_team'] in available_away_teams else 0
        )
        st.session_state['away_team'] = away_team  # 선택된 어웨이팀 저장

        # 출력
        st.subheader(f"{home_team} vs {away_team}")
    else:
        st.write("선택된 리그에 대한 팀 정보가 없습니다.")


    
    # A열부터 X열까지만 처리
    data = data.iloc[:, :24]  # 첫 24개의 열만 선택

    # Google Sheets 데이터 필터링
    filtered_data = data[(data['홈'] == home_team) & (data['원정'] == away_team)]
    # 최근 5개 데이터 추출
    recent_filtered_data = filtered_data.tail(5)

    if not recent_filtered_data.empty:
        recent_result = []
        for _, row in recent_filtered_data.iterrows():
            date = row['경기일정']
            home = row['홈']
            away = row['원정']
            home_goal = row['홈득']
            away_goal = row['원정득']
            vs = 'vs'
            recent_result.append([date, home, home_goal, vs, away_goal, away])

        # DataFrame 생성
        recent_df = pd.DataFrame(recent_result, columns=['일시', '홈', 'H-Goal', '', 'A-Goal', '원정'])


    
    # 홈팀 최근 5경기
    home_filtered_data = data[(data['홈'] == home_team)]
    # 최근 5개 데이터 추출
    home_recent_filtered_data = home_filtered_data.tail(5)

    if not home_recent_filtered_data.empty:
        # df 데이터 생성
        home_recent_result = []
        for _, row in home_recent_filtered_data.iterrows():
            date = row['경기일정']
            home = row['홈']
            away = row['원정']
            home_goal = row['홈득']
            away_goal = row['원정득']
            vs = 'vs'
            home_recent_result.append([date, home, home_goal, vs, away_goal, away])

        # DataFrame 생성
        home_recent_df = pd.DataFrame(home_recent_result, columns=['일시', '홈', 'H-Goal', 'vs', 'A-Goal', '원정'])
    

    # 원정 최근 5경기
    away_filtered_data = data[(data['원정'] == away_team)]
    # 최근 5개 데이터 추출
    away_recent_filtered_data = away_filtered_data.tail(5)

    if not away_recent_filtered_data.empty:
        # df 데이터 생성
        away_recent_result = []
        for _, row in away_recent_filtered_data.iterrows():
            date = row['경기일정']
            home = row['홈']
            away = row['원정']
            home_goal = row['홈득']
            away_goal = row['원정득']
            vs = 'vs'
            away_recent_result.append([date, home, home_goal, vs, away_goal, away])

        # DataFrame 생성
        away_recent_df = pd.DataFrame(away_recent_result, columns=['일시', '홈', 'H-Goal', 'vs', 'A-Goal', '원정'])


    # 홈팀의 경기 (홈 & 원정 경기 전부)
    home_goal_data = data[(data['홈'] == home_team) | (data['원정'] == home_team)]
    # 최근 5개 데이터 추출
    recent_home_goal_data = home_goal_data.tail(5)
    # 원정팀의 경기 (홈 & 원정 경기 전부)
    away_goal_data = data[(data['홈'] == away_team) | (data['원정'] == away_team)]
    # 최근 5개 데이터 추출
    recent_away_goal_data = away_goal_data.tail(5)

    home_gf = []
    for _, row in recent_home_goal_data.iterrows():
        if row['홈'] == home_team:
            home_gf.append(row['홈득'])
        elif row['원정'] == home_team:
            home_gf.append(row['원정득'])
    home_ga = []
    for _, row in recent_home_goal_data.iterrows():
        if row['홈'] == home_team:
            home_ga.append(row['원정득'])
        elif row['원정'] == home_team:
            home_ga.append(row['홈득'])

    away_gf = []
    for _, row in recent_away_goal_data.iterrows():
        if row['홈'] == away_team:
            away_gf.append(row['홈득'])
        elif row['원정'] == away_team:
            away_gf.append(row['원정득'])
    away_ga = []
    for _, row in recent_away_goal_data.iterrows():
        if row['홈'] == away_team:
            away_ga.append(row['원정득'])
        elif row['원정'] == away_team:
            away_ga.append(row['홈득'])






# 통계 선택
stats = ["최근상대전적", "홈_최근5", "원정_최근5", "홈팀 골득실", "원정팀 골득실"]
selected_stats = st.sidebar.multiselect("통계 및 분석 선택", stats, default=stats)

# 한줄 띄기
st.markdown("&nbsp;", unsafe_allow_html=True)

if "최근상대전적" in selected_stats:
    if not filtered_data.empty:
        st.markdown("최근 상대 전적")
        
        # 3번째 열과 5번째 열 중 큰 숫자를 노란색 글씨로 표시
        def highlight_larger(row):
            # 3번째 열과 5번째 열의 값을 가져옵니다.
            col3, col5 = row.iloc[2], row.iloc[4]
            styles = ['' for _ in range(len(row))]  # 기본 스타일은 빈 문자열
            
            if col3 > col5:
                styles[2] = 'color: yellow; font-weight: bold;'  # 3번째 열을 강조
            elif col5 > col3:
                styles[4] = 'color: yellow; font-weight: bold;'  # 5번째 열을 강조
            elif col3 == col5:
                styles[2] = 'color: green; font-weight: bold;'  # 3번째 열을 강조
                styles[4] = 'color: green; font-weight: bold;'  # 5번째 열을 강조
            
            return styles
        
        styled_df = recent_df.style.apply(highlight_larger, axis=1).set_table_styles(
            [{'selector': 'th', 'props': [('text-align', 'center')]},
             {'selector': 'td', 'props': [('text-align', 'center')]}]
        )
        
        # HTML 스타일로 테이블 렌더링
        st.markdown(styled_df.to_html(), unsafe_allow_html=True)

# 줄 긋기
st.markdown("---")

if "홈_최근5" in selected_stats:
    if not home_recent_df.empty:
        st.markdown(f"{home_team} : 최근 홈 5경기")
        
        # 두 번째 열(1번째 인덱스)에 빨간색 스타일 적용
        styled_df = home_recent_df.style.set_table_styles(
            [{'selector': 'th', 'props': [('text-align', 'center')]},
             {'selector': 'td', 'props': [('text-align', 'center')]}]
        ).applymap(lambda x: 'color: red;', subset=pd.IndexSlice[:, home_recent_df.columns[1]])

        # HTML 스타일로 테이블 렌더링
        st.markdown(
            styled_df.to_html(),
            unsafe_allow_html=True
        )
# 한줄 띄기
st.markdown("&nbsp;", unsafe_allow_html=True)
if "원정_최근5" in selected_stats:
    if not away_recent_df.empty:
        st.markdown(f"{away_team} : 최근 원정 5경기")
        
        # 두 번째 열(1번째 인덱스)에 빨간색 스타일 적용
        styled_df = away_recent_df.style.set_table_styles(
            [{'selector': 'th', 'props': [('text-align', 'center')]},
             {'selector': 'td', 'props': [('text-align', 'center')]}]
        ).applymap(lambda x: 'color: blue;', subset=pd.IndexSlice[:, home_recent_df.columns[5]])

        # HTML 스타일로 테이블 렌더링
        st.markdown(
            styled_df.to_html(),
            unsafe_allow_html=True
        )

if "홈팀 골득실" in selected_stats:
    # 그래프 생성
    fig = go.Figure()

    # 홈 득점 데이터 추가
    fig.add_trace(go.Scatter(
        x=list(range(1, len(home_gf) + 1)),  # x축: 최근 경기 순서 (1, 2, 3, ...)
        y=home_gf, 
        mode='lines+markers',
        name='득점',
        line=dict(width=2),
        marker=dict(size=8)
    ))

    # 홈 실점 데이터 추가
    fig.add_trace(go.Scatter(
        x=list(range(1, len(home_ga) + 1)), 
        y=home_ga, 
        mode='lines+markers',
        name='실점',
        line=dict(width=2, dash='dash'),  # 실점은 점선으로 표시
        marker=dict(size=8)
    ))

    # 레이아웃 설정
    fig.update_layout(
        title= f'{home_team} : 최근 5경기 골득실',
        xaxis=dict(
            title= '최근 5경기',
            tickmode= 'linear',  # 눈금 간격을 수동으로 설정
            dtick= 1,           # x축 눈금 간격 1
            range= [1, len(home_gf)]  # x축 범위 설정
        ),
        yaxis=dict(
            title='Goals',
            tickmode='linear',  # 눈금 간격을 수동으로 설정
            dtick=1,           # y축 눈금 간격 1
            range=[0, max(max(home_gf), max(home_ga)) + 1]  # y축 범위 설정
        ),
        height=300,
        legend_title='',
        template='plotly_white'
    )

    # Streamlit에 표시
    st.plotly_chart(fig, use_container_width=True)

if "원정팀 골득실" in selected_stats:
    # 그래프 생성
    fig = go.Figure()

    # 홈 득점 데이터 추가
    fig.add_trace(go.Scatter(
        x=list(range(1, len(away_gf) + 1)),  # x축: 최근 경기 순서 (1, 2, 3, ...)
        y=away_gf, 
        mode='lines+markers',
        name='득점',
        line=dict(width=2),
        marker=dict(size=8)
    ))

    # 홈 실점 데이터 추가
    fig.add_trace(go.Scatter(
        x=list(range(1, len(away_ga) + 1)), 
        y=away_ga, 
        mode='lines+markers',
        name='실점',
        line=dict(width=2, dash='dash'),  # 실점은 점선으로 표시
        marker=dict(size=8)
    ))

    # 레이아웃 설정
    fig.update_layout(
        title= f'{away_team} : 최근 5경기 골득실',
        xaxis=dict(
            title= '최근 5경기',
            tickmode= 'linear',  # 눈금 간격을 수동으로 설정
            dtick= 1,           # x축 눈금 간격 1
            range= [1, len(away_gf)]  # x축 범위 설정
        ),
        yaxis=dict(
            title='Goals',
            tickmode='linear',  # 눈금 간격을 수동으로 설정
            dtick=1,           # y축 눈금 간격 1
            range=[0, max(max(away_gf), max(away_ga)) + 1]  # y축 범위 설정
        ),
        height=300,
        legend_title='',
        template='plotly_white'
    )

    # Streamlit에 표시
    st.plotly_chart(fig, use_container_width=True)
