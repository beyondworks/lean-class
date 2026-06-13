#!/usr/bin/env python3
"""
산출물 생성 헬퍼 - 템플릿을 읽어 프로젝트 폴더에 복사
Usage: python3 generate-artifact.py <artifact-type> <output-path>
Types: prd, trd, ia, userflow, db-schema, business-logic, qa-checklist, all
"""

import sys
import shutil
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = SKILL_DIR / "references" / "templates"

ARTIFACT_MAP = {
    "prd": ("prd-template.json", "PRD.json"),
    "trd": ("trd-template.yaml", "TRD.yaml"),
    "ia": ("ia-template.json", "IA.json"),
    "userflow": ("userflow-template.csv", "UserFlows.csv"),
    "db-schema": ("db-schema-template.sql", "schema.sql"),
    "business-logic": ("business-logic-template.txt", "BusinessLogic.txt"),
    "qa-checklist": ("qa-checklist-template.md", "QA-Checklist.md"),
}

def generate(artifact_type: str, output_path: str):
    out = Path(output_path)
    out.mkdir(parents=True, exist_ok=True)

    if artifact_type == "all":
        types = list(ARTIFACT_MAP.keys())
    elif artifact_type in ARTIFACT_MAP:
        types = [artifact_type]
    else:
        print(f"❌ 알 수 없는 타입: {artifact_type}")
        print(f"   사용 가능: {', '.join(ARTIFACT_MAP.keys())}, all")
        sys.exit(1)

    for t in types:
        src_name, dst_name = ARTIFACT_MAP[t]
        src = TEMPLATES_DIR / src_name
        dst = out / dst_name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"✅ {dst_name} → {dst}")
        else:
            print(f"⚠️  템플릿 없음: {src}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 generate-artifact.py <type|all> <output-path>")
        sys.exit(1)
    generate(sys.argv[1], sys.argv[2])
