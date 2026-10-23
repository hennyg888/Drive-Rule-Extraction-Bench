"""Count modal, condition and vague words on every handbook page (the 10 October keyword scan). Usage: python3 provenance/scripts/scan_keywords.py handbooks/mto"""
import re,html,glob,collections,sys
D=sys.argv[1]
sents=[]
for f in sorted(glob.glob(D+'/*.html')):
  if f.endswith('index.html'): continue
  s=open(f).read(); s=s[s.find('On this page'):] if 'On this page' in s else s
  s=s[:s.find('Updated:')] if 'Updated:' in s else s
  s=re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>','',s)
  s=re.sub(r'<(li|p|h\d|br|tr|td)[^>]*>','\n',s)
  s=html.unescape(re.sub(r'<[^>]+>',' ',s))
  for para in s.split('\n'):
    for x in re.split(r'(?<=[.!?])\s+',re.sub(r'\s+',' ',para).strip()):
      if len(x.split())>=4: sents.append((f.split('/')[-1],x))
print('sentences',len(sents))
P=collections.OrderedDict([
 ('must / must not / required',r'\b(must|are required|is required|have to)\b'),
 ('not permitted / illegal / unlawful / not allowed',r'\b(not permitted|illegal|unlawful|not allowed|prohibited|is an offence|it is against the law)\b'),
 ('may / can (permission)',r'\b(you may|you can|is permitted|are permitted|is allowed|are allowed)\b'),
 ('never / do not / don\'t',r"\b(never|do not|don't)\b"),
 ('should / should not',r'\bshould\b'),
 ('avoid / try to',r'\b(avoid|try to|try not)\b'),
 ('watch for / be careful / be alert / be prepared',r'\b(watch (for|out)|be careful|be alert|be prepared|look out|be aware)\b'),
 ('unless / except',r'\b(unless|except)\b'),
 ('only if / only when / only',r'\bonly\b'),
 ('if / when (condition)',r'^(if|when)\b|\b(if|when) you\b'),
 ('because / so that / to (reason)',r'\b(because|so that|this (will|helps|lets)|otherwise)\b'),
 ('definition (X is a/an/the ...)',r'^(an? |the )?[A-Za-z\- ]{2,40} (is|are) (a|an|the|used|designed|called|special)\b|\bcalled\b|\bmeans\b'),
 ('penalty (fine/demerit/suspend)',r'\b(fine|fined|demerit|suspen|jail|penalt)'),
 ('numeric threshold',r'\b\d+(\.\d+)?\s*(metres|m\b|km/h|seconds|second|kilometres|per cent|%)'),
])
VAGUE=r"\b(safe(ly)?|enough|reasonable|as soon as (you can|possible)|well (before|ahead)|if in doubt|carefully|plenty of|sufficient|properly|proper|too (fast|close)|slowly|gradually|as far (right|left) as (possible|practical)|when (it is )?safe|clear(ly)?|adequate|extra (room|space|care)|suddenly|unexpected)\b"
cnt=collections.Counter(); ex={}
for f,x in sents:
  for k,p in P.items():
    if re.search(p,x,re.I): cnt[k]+=1; ex.setdefault(k,(f,x))
for k in P: print(f'{cnt[k]:5d}  {k}\n       e.g. [{ex.get(k,("",""))[0]}] {ex.get(k,("",""))[1][:160]}')
v=collections.Counter()
for f,x in sents:
  for m in re.finditer(VAGUE,x,re.I): v[m.group(0).lower()]+=1
print('VAGUE',sum(1 for f,x in sents if re.search(VAGUE,x,re.I)),'sentences'); print(v.most_common(25))
none=[(f,x) for f,x in sents if not any(re.search(p,x,re.I) for p in P.values())]
print('unmatched',len(none))
import random; random.seed(1)
for f,x in random.sample(none,25): print(' -',f,'|',x[:150])
