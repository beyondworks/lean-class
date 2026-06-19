"use client";

import { useEffect, useState } from "react";

const slides = [
  {
    kicker: "하루에 영상 50개 제작×업로드",
    title: "월 1회 3시간 투자로 300+ 더 버는",
    product: "AI 숏폼공장 수익화",
    date: "6월 17일 오전 10시 | 6월 18일 오후 7시",
    mentor: "오파독",
    expert: "AI 숏폼공장 수익화 전문가",
    theme: "slide-purple",
    icons: ["instagram", "tiktok", "youtube"],
  },
  {
    kicker: "AI로 95% 자동화",
    title: "8개국 7억명 수출하는",
    product: "K-화장품 해외리셀 부업",
    date: "6월 24일 오전 10시 | 오후 7시",
    mentor: "셀잇파파",
    expert: "AI 해외리셀 전문가",
    theme: "slide-rose",
    icons: ["shop", "spark", "global"],
  },
  {
    kicker: "하루 2시간 세후 월 300+",
    title: "세후 월 300+ 더 버는",
    product: "AI 과일 위탁 부업",
    date: "5월 27일 오전 10시 | 5월 28일 오후 7시",
    mentor: "팜피디",
    expert: "AI 과일 위탁 전문가",
    theme: "slide-green",
    icons: ["fruit", "leaf", "cart"],
  },
];

function HeroBackdrop() {
  return (
    <div className="hero-backdrop-icons" aria-hidden="true">
      <svg viewBox="0 0 84 84">
        <rect x="18" y="12" width="48" height="60" rx="12" />
        <circle cx="42" cy="42" r="13" />
        <path d="M30 22h24" />
      </svg>
      <svg viewBox="0 0 92 92">
        <path d="M24 20h44l8 18-30 38L16 38Z" />
        <path d="M24 38h52M34 20l12 56M58 20 46 76" />
      </svg>
      <svg viewBox="0 0 88 88">
        <rect x="14" y="22" width="60" height="44" rx="12" />
        <path d="m39 35 18 9-18 9Z" />
      </svg>
      <svg viewBox="0 0 78 78">
        <path d="M40 14v36a13 13 0 1 1-10-12" />
        <path d="M40 18c6 10 12 14 22 15" />
      </svg>
      <svg viewBox="0 0 82 82">
        <path d="M16 54c12-30 34-38 50-24-4 24-22 38-50 24Z" />
        <path d="M24 51c14-10 25-16 38-18" />
      </svg>
    </div>
  );
}

function SlideIcon({ type, index }: { type: string; index: number }) {
  return (
    <div className={`social social-${index} ${type}`} aria-hidden="true">
      {type === "instagram" ? "◎" : null}
      {type === "tiktok" ? "♪" : null}
      {type === "youtube" ? "▶" : null}
      {type === "shop" ? "S" : null}
      {type === "spark" ? "✦" : null}
      {type === "global" ? "G" : null}
      {type === "fruit" ? "●" : null}
      {type === "leaf" ? "L" : null}
      {type === "cart" ? "C" : null}
    </div>
  );
}

export function HeroSlider() {
  const [current, setCurrent] = useState(0);
  const slide = slides[current];

  useEffect(() => {
    const timer = window.setInterval(() => {
      setCurrent((value) => (value + 1) % slides.length);
    }, 4800);

    return () => window.clearInterval(timer);
  }, []);

  const move = (direction: number) => {
    setCurrent((value) => (value + direction + slides.length) % slides.length);
  };

  return (
    <div className={`hero-shell ${slide.theme}`}>
      <HeroBackdrop />
      <div className="hero-inner">
        <div className="hero-copy">
          <p>{slide.kicker}</p>
          <h1>
            {slide.title}
            <br />
            {slide.product}
          </h1>
          <div className="date-chip">{slide.date}</div>
        </div>
        <div className="hero-media" aria-label={`${slide.mentor} 강사`}>
          <div className="social-cluster">
            {slide.icons.map((icon, index) => (
              <SlideIcon key={icon} type={icon} index={index} />
            ))}
          </div>
          <img src="/assets/instructor-hero.png" alt={`${slide.mentor} 강사 이미지`} />
          <p>
            {slide.mentor}
            <span>{slide.expert}</span>
          </p>
        </div>
        <div className="slider" aria-label="히어로 슬라이드">
          <button type="button" onClick={() => move(-1)} aria-label="이전 히어로">
            ‹
          </button>
          {slides.map((item, index) => (
            <button
              key={item.product}
              type="button"
              className={index === current ? "active" : ""}
              onClick={() => setCurrent(index)}
              aria-label={`${index + 1}번째 히어로`}
            />
          ))}
          <button type="button" onClick={() => move(1)} aria-label="다음 히어로">
            ›
          </button>
        </div>
      </div>
    </div>
  );
}
