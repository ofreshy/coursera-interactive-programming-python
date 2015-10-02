# codeskulptor http://www.codeskulptor.org/#user40_TednMc01Sn_0.py
ro = "Rock"
li = "Lizard"
pa = "Paper"
sc = "Scissors"
sp = "Spock"
wins = {
  ro: (li, sc),
  li: (pa, sp),
  pa: (sp, ro),
  sc: (pa, li)
  sp: (ro, sc),
}

# who wins
def is_p1_winner(p1, p2):
    return p2 in wins[p1]
