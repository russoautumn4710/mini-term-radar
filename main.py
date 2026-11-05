import re
from collections import Counter

KNOWN = {'openai', 'claude', 'python', 'github', 'hugging', 'face', 'agent', 'llm', 'ai', 'model', 'models', 'code'}
STOP = {'the', 'and', 'for', 'with', 'from', 'that', 'this', 'into', 'your', 'about', 'new', 'daily', 'using', 'built', 'open', 'source', 'design', 'system', 'terms'}

def terms(text):
    words = re.findall(r'[A-Za-z][A-Za-z0-9-]{2,}', text.lower())
    return [w for w in words if w not in STOP and w not in KNOWN]

def score(texts):
    counts = Counter()
    first_seen = {}
    for i, text in enumerate(texts):
        for term in set(terms(text)):
            counts[term] += 1
            if term not in first_seen:
                first_seen[term] = i
    ranked = []
    for term, c in counts.items():
        novelty = 1.0 / (1 + first_seen[term])
        score = c * (1 + novelty)
        ranked.append((round(score, 2), term, c))
    return sorted(ranked, reverse=True)

def main():
    posts = [
        'OpenAI launches new o3 model and agent tool for coding',
        'New repo solid-glass is a design system for AI apps',
        'DeepSeek harness makes claude-code skills popular',
        'Indra OCR model runs on CPU and parses PDF documents',
        'OpenUI powers streaming generative-ui answers in Nextjs',
        'AI agents use mcp server for keyword research and trends'
    ]
    top = score(posts)[:8]
    print('AI New-Term Radar Demo')
    for s, term, c in top:
        print(f'{term:15s} freq={c} score={s}')

if __name__ == '__main__':
    main()
