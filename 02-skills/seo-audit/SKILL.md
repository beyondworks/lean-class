---
name: seo-audit
description: Audit, review, or diagnose SEO issues on websites. Use when the user mentions "SEO audit", "technical SEO", "why am I not ranking", "SEO issues", "on-page SEO", "meta tags review", or "SEO health check". For building pages at scale, see programmatic-seo.
metadata:
  author: coreyhaines31
  version: "1.0.0"
allowed-tools: []
---

# SEO Audit

Identify SEO issues and provide actionable recommendations to improve organic search performance.

## Initial Assessment

Before auditing, understand:

1. **Site Context**: Type (SaaS, e-commerce, blog)? Primary SEO goal? Priority keywords?
2. **Current State**: Known issues? Current traffic? Recent changes?
3. **Scope**: Full site or specific pages? Technical + on-page or focused?

---

## Audit Priority Order

1. **Crawlability & Indexation** - Can Google find and index it?
2. **Technical Foundations** - Is the site fast and functional?
3. **On-Page Optimization** - Is content optimized?
4. **Content Quality** - Does it deserve to rank?

---

## Technical SEO

### Crawlability

- **Robots.txt**: Check for unintentional blocks, verify sitemap reference
- **XML Sitemap**: Exists, accessible, contains only canonical URLs
- **Architecture**: Important pages within 3 clicks, no orphan pages

### Indexation

- **site:domain.com** check
- Noindex on important pages?
- Canonical issues?
- Redirect chains/loops?
- Duplicate content?

### Core Web Vitals

- **LCP** < 2.5s
- **INP** < 200ms
- **CLS** < 0.1

### Mobile & Security

- Responsive design (not separate m. site)
- HTTPS across entire site
- Valid SSL, no mixed content

---

## On-Page SEO

### Title Tags

- Unique per page, primary keyword near beginning
- 50-60 characters, compelling, brand at end

### Meta Descriptions

- Unique per page, 150-160 characters
- Includes keyword, clear value prop, CTA

### Heading Structure

- One H1 per page with primary keyword
- Logical hierarchy (H1 → H2 → H3)

### Content

- Keyword in first 100 words
- Sufficient depth for topic
- Answers search intent
- Better than competitors

### Images

- Descriptive file names and alt text
- Compressed, modern formats (WebP)
- Lazy loading, responsive

### Internal Linking

- Important pages well-linked
- Descriptive anchor text
- No orphan pages

---

## Content Quality (E-E-A-T)

- **Experience**: First-hand experience, original insights
- **Expertise**: Author credentials visible, accurate info
- **Authoritativeness**: Recognized in space, cited by others
- **Trustworthiness**: Contact info, privacy policy, HTTPS

---

## Common Issues by Site Type

### SaaS/Product

- Product pages lack depth
- Missing comparison/alternative pages
- No educational content

### E-commerce

- Thin category pages
- Duplicate product descriptions
- Missing product schema

### Content/Blog

- Outdated content
- Keyword cannibalization
- Poor internal linking

### Local Business

- Inconsistent NAP
- Missing local schema
- No Google Business Profile optimization

---

## Output Format

**Executive Summary**

- Overall health (Good/Needs Work/Critical)
- Top 3-5 priority issues
- Quick wins

**Findings** (for each issue):

- **Issue**: What's wrong
- **Impact**: High/Medium/Low
- **Evidence**: How found
- **Fix**: Specific recommendation
- **Priority**: 1-5

**Prioritized Action Plan**

1. Critical fixes (blocking indexation)
2. High-impact improvements
3. Quick wins
4. Long-term recommendations

---

## Related Skills

- **programmatic-seo**: Building SEO pages at scale
- **schema-markup**: Structured data implementation
