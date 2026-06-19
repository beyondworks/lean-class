import { HeroSlider } from "./components/HeroSlider";

const freeCourses = [
  {
    title: "AI 숏폼 공장 수익화 무료강의",
    mentor: "오파독",
    expert: "AI 숏폼 공장 수익화 전문가",
    date: "6월 17일 오전 10시 | 6월 18일 오후 7시",
    tag: "AI 숏폼공장 수익화",
    theme: "purple",
    status: "모집중",
  },
  {
    title: "AI K-화장품 해외리셀 부업 무료강의",
    mentor: "셀잇파파",
    expert: "AI 해외리셀 전문가",
    date: "6월 24일 오전 10시 | 오후 7시",
    tag: "K-화장품 해외리셀 부업",
    theme: "rose",
    status: "모집중",
  },
  {
    title: "AI 과일 위탁 부업 무료강의",
    mentor: "팜피디",
    expert: "AI 과일 위탁 전문가",
    date: "5월 27일 오전 10시 | 5월 28일 오후 7시",
    tag: "AI 과일 위탁 부업",
    theme: "green",
    status: "모집마감",
  },
];

const premiumCourses = [
  {
    title: "AI 숏폼 공장 수익화 정규강의",
    mentor: "오파독",
    expert: "AI 숏폼 공장 수익화 전문가",
    date: "한정인원 선착순 할인",
    tag: "AI 숏폼공장 수익화",
    theme: "purple",
    status: "모집중",
  },
  {
    title: "AI 과일 위탁 부업 정규강의",
    mentor: "팜피디",
    expert: "AI 과일 위탁 전문가",
    date: "한정인원 선착순 오픈",
    tag: "AI 과일 위탁 부업",
    theme: "green",
    status: "모집마감",
  },
  {
    title: "네이버 연결 부업 정규강의",
    mentor: "다퍼주는남자",
    expert: "네이버 연결 수익화 전문가",
    date: "한정인원 선착순 오픈",
    tag: "AI 네이버 연결 부업",
    theme: "naver",
    status: "모집마감",
  },
];

const scheduleItems = [
  ["2026-06", "24(수)", "AI K-화장품 해외리셀 부업 무료강의 (1차)", "open"],
  ["2026-06", "24(수)", "AI K-화장품 해외리셀 부업 무료강의 (2차)", "open"],
  ["2026-05", "27(수)", "AI 과일 위탁 부업 무료강의 (1차)", "closed"],
  ["2026-05", "28(목)", "AI 과일 위탁 부업 무료강의 (2차)", "closed"],
  ["2026-06", "17(수)", "AI 숏폼 공장 수익화 무료강의 (1차)", "closed"],
];

const instructors = ["유튜브 수익화의 귀재", "이원자탄소", "셀잇파파", "다퍼남", "픽지쌤", "유튜브 수익화의 귀재"];

function BrandMark() {
  return (
    <span className="brand-mark" aria-hidden="true">
      <i />
      <i />
      <i />
    </span>
  );
}

function CourseCard({
  course,
}: {
  course: {
    title: string;
    mentor: string;
    expert: string;
    date: string;
    tag: string;
    theme: string;
    status: string;
  };
}) {
  return (
    <article className="course">
      <div className={`poster ${course.theme}`}>
        <div className="poster-date">{course.date}</div>
        <span className={course.status === "모집중" ? "status open" : "status"}>{course.status}</span>
        <div className="poster-copy">
          <small>월 1회 3시간 투자로</small>
          <strong>{course.tag}</strong>
        </div>
        <div className="live-row">
          <span>LIVE</span>
          <b>라이브 무료 강의</b>
        </div>
        <img src="/assets/instructor-hero.png" alt="" />
        <em>{course.mentor}</em>
      </div>
      <h3>{course.title}</h3>
      <p>
        {course.mentor} | {course.expert}
      </p>
    </article>
  );
}

function CourseSection({
  title,
  courses,
}: {
  title: string;
  courses: typeof freeCourses;
}) {
  return (
    <section className="section">
      <div className="section-head">
        <h2>
          <BrandMark />
          {title}
        </h2>
        <a href="#">전체 보기</a>
      </div>
      <div className="grid">
        {courses.map((course) => (
          <CourseCard key={course.title} course={course} />
        ))}
      </div>
    </section>
  );
}

export default function Home() {
  return (
    <main>
      <section className="hero">
        <nav className="nav" aria-label="머니루트 주요 메뉴">
          <a className="brand" href="#">
            <BrandMark />
            <strong>머니루트</strong>
          </a>
          <div className="nav-links">
            <a href="#free">무료강의</a>
            <a href="#premium">프리미엄 강의</a>
            <a href="#reviews">수강후기</a>
            <a href="#apply">강사지원</a>
          </div>
          <div className="nav-actions">
            <a href="#support">고객문의</a>
            <button type="button">로그인</button>
          </div>
        </nav>

        <HeroSlider />
      </section>

      <div className="content">
        <div id="free">
          <CourseSection title="무료 강의" courses={freeCourses} />
        </div>
        <div id="premium">
          <CourseSection title="프리미엄 강의" courses={premiumCourses} />
        </div>

        <section className="section upcoming">
          <div className="section-head">
            <h2>
              <BrandMark />
              오픈 예정
            </h2>
          </div>
          <div className="upcoming-grid">
            {["AI 코스트코 부업", "AI 블로그 연결 부업"].map((item) => (
              <article key={item}>
                <div>
                  <span>COMING</span>
                  <span>SOON</span>
                </div>
                <h3>{item}</h3>
                <p>수익화 전문가</p>
              </article>
            ))}
          </div>
        </section>

        <section className="section schedule">
          <div className="section-head">
            <h2>
              <BrandMark />
              무료강의 일정
            </h2>
          </div>
          <div className="schedule-layout">
            <article className="calendar">
              <header>
                <button type="button">‹</button>
                <strong>2026. 6</strong>
                <button type="button">›</button>
              </header>
              <div className="week">
                {["일", "월", "화", "수", "목", "금", "토"].map((day) => (
                  <span key={day}>{day}</span>
                ))}
              </div>
              <div className="days">
                {Array.from({ length: 30 }, (_, index) => index + 1).map((day) => (
                  <span key={day} className={day === 19 ? "today" : day === 17 || day === 18 ? "dot" : ""}>
                    {day}
                  </span>
                ))}
              </div>
            </article>
            <article className="schedule-list">
              {scheduleItems.map(([month, day, title, state]) => (
                <div key={`${day}-${title}`} className={state}>
                  <small>
                    {month}
                    <b>{day}</b>
                  </small>
                  <strong>{title}</strong>
                  {state === "closed" ? <span>마감</span> : null}
                </div>
              ))}
            </article>
          </div>
        </section>

        <section className="instructors">
          <h2>
            <BrandMark />
            머니루트 강사
          </h2>
          <div className="rail">
            {instructors.map((name, index) => (
              <article key={`${name}-${index}`}>
                <img src="/assets/generated-instructors.png" alt="" />
                <strong>{name}</strong>
              </article>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}
