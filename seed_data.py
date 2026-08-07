from database import execute_query

print("Clearing existing data...")

execute_query("""
MATCH (n)
DETACH DELETE n
""")

print("Creating Genres...")

execute_query("""
CREATE
(:Genre {name:'Action'}),
(:Genre {name:'Drama'}),
(:Genre {name:'Sci-Fi'}),
(:Genre {name:'Adventure'}),
(:Genre {name:'Thriller'}),
(:Genre {name:'Fantasy'}),
(:Genre {name:'Comedy'}),
(:Genre {name:'Crime'})
""")

print("Creating Actors...")

execute_query("""
CREATE
(:Actor {name:'Yash'}),
(:Actor {name:'Allu Arjun'}),
(:Actor {name:'Ram Charan'}),
(:Actor {name:'Jr NTR'}),
(:Actor {name:'Prabhas'}),
(:Actor {name:'Robert Downey Jr.'}),
(:Actor {name:'Chris Evans'}),
(:Actor {name:'Tom Holland'}),
(:Actor {name:'Scarlett Johansson'}),
(:Actor {name:'Chris Hemsworth'})
""")

print("Creating Directors...")

execute_query("""
CREATE
(:Director {name:'Prashanth Neel'}),
(:Director {name:'Sukumar'}),
(:Director {name:'S. S. Rajamouli'}),
(:Director {name:'Anthony Russo'}),
(:Director {name:'Joe Russo'}),
(:Director {name:'Jon Watts'})
""")

print("Part 1 Completed Successfully")
print("Creating Movies...")

execute_query("""
CREATE
(m1:Movie {title:'KGF', year:2018}),
(m2:Movie {title:'KGF Chapter 2', year:2022}),
(m3:Movie {title:'Pushpa', year:2021}),
(m4:Movie {title:'Pushpa 2', year:2024}),
(m5:Movie {title:'RRR', year:2022}),
(m6:Movie {title:'Salaar', year:2023}),
(m7:Movie {title:'Baahubali', year:2015}),
(m8:Movie {title:'Baahubali 2', year:2017}),
(m9:Movie {title:'Iron Man', year:2008}),
(m10:Movie {title:'Captain America', year:2011}),
(m11:Movie {title:'Avengers', year:2012}),
(m12:Movie {title:'Avengers Endgame', year:2019}),
(m13:Movie {title:'Spider-Man Homecoming', year:2017}),
(m14:Movie {title:'Spider-Man No Way Home', year:2021}),
(m15:Movie {title:'Thor Ragnarok', year:2017})
""")

print("Movies Created Successfully")

print("Creating Relationships...")

execute_query("""
MATCH (kgf:Movie {title:'KGF'})
MATCH (kgf2:Movie {title:'KGF Chapter 2'})
MATCH (pushpa:Movie {title:'Pushpa'})
MATCH (pushpa2:Movie {title:'Pushpa 2'})
MATCH (rrr:Movie {title:'RRR'})
MATCH (salaar:Movie {title:'Salaar'})
MATCH (bb1:Movie {title:'Baahubali'})
MATCH (bb2:Movie {title:'Baahubali 2'})
MATCH (iron:Movie {title:'Iron Man'})
MATCH (cap:Movie {title:'Captain America'})
MATCH (av:Movie {title:'Avengers'})
MATCH (end:Movie {title:'Avengers Endgame'})
MATCH (sp1:Movie {title:'Spider-Man Homecoming'})
MATCH (sp2:Movie {title:'Spider-Man No Way Home'})
MATCH (thor:Movie {title:'Thor Ragnarok'})

MATCH (action:Genre {name:'Action'})
MATCH (drama:Genre {name:'Drama'})
MATCH (adventure:Genre {name:'Adventure'})
MATCH (scifi:Genre {name:'Sci-Fi'})
MATCH (fantasy:Genre {name:'Fantasy'})

MATCH (yash:Actor {name:'Yash'})
MATCH (allu:Actor {name:'Allu Arjun'})
MATCH (ram:Actor {name:'Ram Charan'})
MATCH (ntr:Actor {name:'Jr NTR'})
MATCH (prabhas:Actor {name:'Prabhas'})
MATCH (rdj:Actor {name:'Robert Downey Jr.'})
MATCH (evans:Actor {name:'Chris Evans'})
MATCH (tom:Actor {name:'Tom Holland'})
MATCH (scarlett:Actor {name:'Scarlett Johansson'})
MATCH (hemsworth:Actor {name:'Chris Hemsworth'})

MATCH (pn:Director {name:'Prashanth Neel'})
MATCH (suku:Director {name:'Sukumar'})
MATCH (ssr:Director {name:'S. S. Rajamouli'})
MATCH (russo:Director {name:'Anthony Russo'})
MATCH (watts:Director {name:'Jon Watts'})

CREATE

(kgf)-[:BELONGS_TO]->(action),
(kgf2)-[:BELONGS_TO]->(action),
(pushpa)-[:BELONGS_TO]->(action),
(pushpa2)-[:BELONGS_TO]->(action),
(rrr)-[:BELONGS_TO]->(drama),
(salaar)-[:BELONGS_TO]->(action),
(bb1)-[:BELONGS_TO]->(adventure),
(bb2)-[:BELONGS_TO]->(adventure),
(iron)-[:BELONGS_TO]->(scifi),
(cap)-[:BELONGS_TO]->(action),
(av)-[:BELONGS_TO]->(scifi),
(end)-[:BELONGS_TO]->(scifi),
(sp1)-[:BELONGS_TO]->(action),
(sp2)-[:BELONGS_TO]->(action),
(thor)-[:BELONGS_TO]->(fantasy),

(kgf)-[:ACTED_IN]->(yash),
(kgf2)-[:ACTED_IN]->(yash),
(pushpa)-[:ACTED_IN]->(allu),
(pushpa2)-[:ACTED_IN]->(allu),
(rrr)-[:ACTED_IN]->(ram),
(rrr)-[:ACTED_IN]->(ntr),
(salaar)-[:ACTED_IN]->(prabhas),
(bb1)-[:ACTED_IN]->(prabhas),
(bb2)-[:ACTED_IN]->(prabhas),
(iron)-[:ACTED_IN]->(rdj),
(cap)-[:ACTED_IN]->(evans),
(av)-[:ACTED_IN]->(scarlett),
(sp1)-[:ACTED_IN]->(tom),
(sp2)-[:ACTED_IN]->(tom),
(thor)-[:ACTED_IN]->(hemsworth),

(kgf)-[:DIRECTED_BY]->(pn),
(kgf2)-[:DIRECTED_BY]->(pn),
(salaar)-[:DIRECTED_BY]->(pn),
(pushpa)-[:DIRECTED_BY]->(suku),
(pushpa2)-[:DIRECTED_BY]->(suku),
(rrr)-[:DIRECTED_BY]->(ssr),
(bb1)-[:DIRECTED_BY]->(ssr),
(bb2)-[:DIRECTED_BY]->(ssr),
(iron)-[:DIRECTED_BY]->(russo),
(av)-[:DIRECTED_BY]->(russo),
(end)-[:DIRECTED_BY]->(russo),
(sp1)-[:DIRECTED_BY]->(watts),
(sp2)-[:DIRECTED_BY]->(watts)
""")

print("Relationships Created Successfully")
print("Creating Users...")

execute_query("""
CREATE
(u1:User {name:'Krishna'}),
(u2:User {name:'Rahul'}),
(u3:User {name:'Priya'}),
(u4:User {name:'Arjun'}),
(u5:User {name:'Sneha'})
""")

print("Creating WATCHED Relationships...")

execute_query("""
MATCH (u1:User {name:'Krishna'})
MATCH (u2:User {name:'Rahul'})
MATCH (u3:User {name:'Priya'})
MATCH (u4:User {name:'Arjun'})
MATCH (u5:User {name:'Sneha'})

MATCH (kgf:Movie {title:'KGF'})
MATCH (kgf2:Movie {title:'KGF Chapter 2'})
MATCH (pushpa:Movie {title:'Pushpa'})
MATCH (pushpa2:Movie {title:'Pushpa 2'})
MATCH (rrr:Movie {title:'RRR'})
MATCH (salaar:Movie {title:'Salaar'})
MATCH (bb2:Movie {title:'Baahubali 2'})
MATCH (end:Movie {title:'Avengers Endgame'})
MATCH (sp2:Movie {title:'Spider-Man No Way Home'})

CREATE
(u1)-[:WATCHED]->(kgf),
(u1)-[:WATCHED]->(kgf2),
(u1)-[:WATCHED]->(salaar),

(u2)-[:WATCHED]->(pushpa),
(u2)-[:WATCHED]->(pushpa2),

(u3)-[:WATCHED]->(rrr),
(u3)-[:WATCHED]->(bb2),

(u4)-[:WATCHED]->(end),
(u4)-[:WATCHED]->(sp2),

(u5)-[:WATCHED]->(kgf),
(u5)-[:WATCHED]->(rrr),
(u5)-[:WATCHED]->(pushpa)
""")

print("Users and WATCHED relationships created successfully!")