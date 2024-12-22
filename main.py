# main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd
import matplotlib.pyplot as plt
import random

app = FastAPI()

# 장르별 추천 영화 더미 데이터
movies_data = {
    "액션": "범죄도시",
    "코미디": "극한직업",
    "드라마": "변호인",
    "판타지": "신과함께",
    "스릴러": "파묘",
    "공포": "장산범",
    "애니메이션": "날씨의 아이",
}

# 가짜 영화 데이터 생성
def fake_movie_data(num_movies=100):
    genres = list(movies_data.keys())
    movies = []
    
    for _ in range(num_movies):
        movie_name = f"영화_{random.randint(1, 1000)}"
        genre = random.choice(genres)
        movies.append({"title": movie_name, "genre": genre})
    
    return movies

@app.get("/", response_class=HTMLResponse)
async def show_movies():
    # 영화 데이터 생성 (매번 새로운 데이터 생성)
    movies = fake_movie_data()

    # 데이터프레임으로 변환
    df = pd.DataFrame(movies)

    # 장르별 영화 수 계산
    genre_counts = df['genre'].value_counts()

    # 막대 그래프 생성
    plt.figure(figsize=(10, 6))
    plt.rc('font', family='Apple SD Gothic Neo')  # 맥에서 한글 폰트 설정
    genre_counts.plot(kind='bar', color='skyblue')
    plt.title('장르별 영화 수', fontsize=16)
    plt.xlabel('장르', fontsize=14)
    plt.ylabel('영화 수', fontsize=14)
    plt.xticks(rotation=45, fontsize=12)

    # 그래프 저장
    plt.tight_layout()
    graph_path = "movie_genres.png"
    plt.savefig(graph_path)
    plt.close()

    # 가장 높은 장르 찾기
    top_genre = genre_counts.idxmax()
    recommended_movie = movies_data[top_genre]

    # HTML 페이지 생성
    html_content = f"""
    <html>
        <head>
            <title>영화 추천 시스템</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; }}
                img {{ margin-top: 20px; }}
                table {{ margin: 20px auto; border-collapse: collapse; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>영화 추천 시스템</h1>
            <h2>장르별 영화 수</h2>
            <img src="/static/{graph_path}" alt="장르별 영화 수 그래프">
            
            <h2>추천 영화 ({top_genre} 장르)</h2>
            <p>{recommended_movie}</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/static/{file_path:path}")
async def get_graph(file_path: str):
    return HTMLResponse(content=open(file_path, "rb").read(), media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
