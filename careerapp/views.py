import json
import os
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests
from datetime import datetime
import difflib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SKILLS_FILE = os.path.join(BASE_DIR, "skills.json")
SUBMISSIONS_FILE = os.path.join(BASE_DIR, "submissions.json")


def index(request):
    """Render main page."""
    return render(request, "index.html")


# ---------------------------
# Smart role matching helper
# ---------------------------
def smart_match_role(user_input, skills_map):
    """
    Try several strategies to map user_input to a known role key in skills_map.
    Returns the matched role string (one of the keys of skills_map) or None.
    """
    if not user_input:
        return None

    # Normalize
    ui = user_input.strip()
    ui_lower = ui.lower()

    # 1) Exact match (case-sensitive)
    if ui in skills_map:
        return ui

    # 2) Exact case-insensitive match
    for role in skills_map.keys():
        if role.lower() == ui_lower:
            return role

    # 3) Substring match (user input contained in role name)
    for role in skills_map.keys():
        if ui_lower in role.lower():
            return role

    # 4) Role keywords match (every word in user input appears in role)
    ui_words = [w for w in ui_lower.split() if w]
    if ui_words:
        for role in skills_map.keys():
            role_words = role.lower().split()
            if all(any(w in rw for rw in role_words) for w in ui_words):
                return role

    # 5) Fuzzy match using difflib (for typos / short forms)
    role_names = list(skills_map.keys())
    # allow small cutoff for similarity
    matches = difflib.get_close_matches(ui, role_names, n=1, cutoff=0.6)
    if matches:
        return matches[0]

    # 6) Try fuzzy on lowercase names
    lower_to_role = {r.lower(): r for r in role_names}
    matches = difflib.get_close_matches(ui_lower, list(lower_to_role.keys()), n=1, cutoff=0.6)
    if matches:
        return lower_to_role[matches[0]]

    return None


# ---------------------------
# API: Skill Gap
# ---------------------------
@csrf_exempt
def api_skill_gap(request):
    """
    POST JSON:
    {
      "targetRole": "Frontend Developer",
      "currentSkills": ["HTML","CSS"]
    }
    Response:
      requiredSkills, matched, missing, recommendations, suggestedOrder
    """
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST allowed.")

    try:
        body = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("Invalid JSON payload.")

    target = (body.get("targetRole") or "").strip()
    current = body.get("currentSkills", [])

    # accept comma-separated string too
    if isinstance(current, str):
        current = [s.strip() for s in current.split(",") if s.strip()]

    # load skills mapping
    try:
        with open(SKILLS_FILE, "r", encoding="utf-8") as f:
            skills_map = json.load(f)
    except Exception:
        return JsonResponse({"error": "Server: skills data not available"}, status=500)

    # smart match user input to a known role key
    matched_role = smart_match_role(target, skills_map)

    if not matched_role:
        # helpful response: suggest available roles
        return JsonResponse({
            "error": f"Role '{target}' not found",
            "available_roles": list(skills_map.keys())
        }, status=400)

    required = skills_map[matched_role]

    # normalize matching (case-insensitive)
    req_lower = [r.lower() for r in required]
    current_norm = [c.strip() for c in current if c.strip()]
    cur_lower = [c.lower() for c in current_norm]

    matched = [required[i] for i, r in enumerate(req_lower) if r in cur_lower]
    missing = [s for s in required if s.lower() not in cur_lower]

    recommendations = [
        {
            "skill": m,
            "why": f"{m} is commonly required for {matched_role}",
            "source": f"Search 'learn {m}' on YouTube/documentation"
        } for m in missing
    ]

    suggested_order = missing[:]  # simple ordering: as listed in skills.json

    # optionally append submission to local JSON store
    try:
        submission = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "requestedRole": target,
            "matchedRole": matched_role,
            "currentSkills": current_norm
        }
        if os.path.exists(SUBMISSIONS_FILE):
            with open(SUBMISSIONS_FILE, "r+", encoding="utf-8") as sf:
                try:
                    arr = json.load(sf)
                except Exception:
                    arr = []
                arr.append(submission)
                sf.seek(0)
                json.dump(arr, sf, indent=2)
                sf.truncate()
    except Exception:
        # don't fail the API if saving fails
        pass

    return JsonResponse({
        "requiredSkills": required,
        "matched": matched,
        "missing": missing,
        "recommendations": recommendations,
        "suggestedOrder": suggested_order,
        "matchedRole": matched_role
    })


# ---------------------------
# API: Roadmap
# ---------------------------
@csrf_exempt
def api_roadmap(request):
    """
    POST JSON: { "targetRole": "Backend Developer" }
    Returns a 3-step roadmap (mock logic)
    """
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST allowed.")

    try:
        body = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("Invalid JSON payload.")

    target = (body.get("targetRole") or "").strip()

    # load skill map to help match
    try:
        with open(SKILLS_FILE, "r", encoding="utf-8") as f:
            skills_map = json.load(f)
    except Exception:
        skills_map = {}

    matched_role = smart_match_role(target, skills_map) if target else None

    mock_roadmaps = {
        "Frontend Developer": [
            "Phase 1 (1–2 months): HTML, CSS, Git",
            "Phase 2 (2 months): JavaScript, React, State Management",
            "Phase 3 (1–2 months): Projects, API Integration, Deployment"
        ],
        "Backend Developer": [
            "Phase 1 (1–2 months): Language basics, SQL, Git",
            "Phase 2 (2 months): Framework (Django/Spring), REST APIs",
            "Phase 3 (1–2 months): Auth, Caching, Deployment, Projects"
        ],
        "Full Stack Developer": [
            "Phase 1 (1–2 months): Frontend fundamentals (HTML/CSS/JS)",
            "Phase 2 (2 months): React + Backend (Django) + APIs",
            "Phase 3 (1–2 months): Full projects, deployment, CI/CD basics"
        ],
        "Data Analyst": [
            "Phase 1 (1–2 months): Excel, SQL",
            "Phase 2 (2 months): Python, Pandas, Visualization",
            "Phase 3 (1–2 months): Statistics, Dashboards, Projects"
        ],
        "Machine Learning Engineer": [
            "Phase 1 (1–2 months): Python, Math & Statistics fundamentals",
            "Phase 2 (2 months): ML algorithms, Scikit-Learn, Projects",
            "Phase 3 (1–2 months): Deep Learning basics (TensorFlow), deployment"
        ]
    }

    roadmap = mock_roadmaps.get(matched_role, [
        "Phase 1: Learn fundamentals",
        "Phase 2: Build core competency",
        "Phase 3: Create projects + deploy"
    ])

    return JsonResponse({"roadmap": roadmap})


# ---------------------------
# HackerNews integration
# ---------------------------
def _hn_time_to_iso(ts):
    try:
        return datetime.utcfromtimestamp(ts).isoformat() + "Z"
    except Exception:
        return None


def _fetch_hackernews_top5():
    top_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    try:
        r = requests.get(top_url, timeout=8)
        r.raise_for_status()
        ids = r.json()[:20]
    except Exception:
        return []

    stories = []
    for idn in ids:
        try:
            s = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{idn}.json", timeout=6).json()
            if not s:
                continue
            if s.get("type") != "story":
                continue
            stories.append({
                "id": s.get("id"),
                "title": s.get("title"),
                "url": s.get("url"),
                "score": s.get("score"),
                "time": _hn_time_to_iso(s.get("time")) if s.get("time") else None,
                "type": s.get("type"),
                "by": s.get("by")
            })
            if len(stories) >= 5:
                break
        except Exception:
            continue
    return stories


def api_news(request):
    if request.method != "GET":
        return HttpResponseBadRequest("Only GET allowed.")
    stories = _fetch_hackernews_top5()
    return JsonResponse(stories, safe=False)
