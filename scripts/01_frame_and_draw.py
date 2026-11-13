import os
os.makedirs("output",exist_ok=True)
def src(n):
    return "output/"+n if os.path.exists("output/"+n) else "data/"+n
import csv, random

# Pitchfork year-end top 50s, 2006-2011 (muzieklijstjes.nl for 2006-2010, BrooklynVegan for 2011)
L = {}
L[2006] = """Knife|Silent Shout
TV on the Radio|Return to Cookie Mountain
Joanna Newsom|Ys
Ghostface Killah|Fishscale
The Hold Steady|Boys and Girls in America
Liars|Drum's Not Dead
Clipse|Hell Hath No Fury
Grizzly Bear|Yellow House
Boris|Pink
Scott Walker|The Drift
Junior Boys|So This Is Goodbye
Band of Horses|Everything All the Time
Phoenix|It's Never Been Like That
Tim Hecker|Harmony in Ultraviolet
Sunset Rubdown|Shut Up I Am Dreaming
Beach House|Beach House
The Thermals|The Body, the Blood, the Machine
Destroyer|Destroyer's Rubies
T.I.|King
Man Man|Six Demon Bag
Be Your Own Pet|Be Your Own Pet
LCD Soundsystem|LCD Soundsystem [listed as 2004 release]
Yo La Tengo|I Am Not Afraid of You and I Will Beat Your Ass
Peter Bjorn and John|Writer's Block
Justin Timberlake|FutureSex/LoveSounds
Hot Chip|The Warning
Califone|Roots & Crowns
Cat Power|The Greatest
Lily Allen|Alright, Still
Belle and Sebastian|The Life Pursuit
Danielson|Ships
Lupe Fiasco|Food & Liquor
Mission of Burma|The Obliterati
Girl Talk|Night Ripper
Herbert|Scale
Brightblack Morning Light|Brightblack Morning Light
DJ Drama|Dedication 2
J Dilla|Donuts
Fujiya & Miyagi|Transparent Things
Tapes 'n Tapes|The Loon
The Decemberists|The Crane Wife
Mastodon|Blood Mountain
Sonic Youth|Rather Ripped
The Pipettes|We Are the Pipettes
Camera Obscura|Let's Get Out of This Country
M. Ward|Post-War
Matmos|The Rose Has Teeth in the Mouth of a Beast
The Long Blondes|Someone to Drive You Home
Ellen Allien & Apparat|Orchestra of Bubbles
Booka Shade|Movements"""
L[2007] = """Panda Bear|Person Pitch
LCD Soundsystem|Sound of Silver
M.I.A.|Kala
Radiohead|In Rainbows
Of Montreal|Hissing Fauna, Are You the Destroyer?
Animal Collective|Strawberry Jam
Spoon|Ga Ga Ga Ga Ga
Battles|Mirrored
The Field|From Here We Go Sublime
Burial|Untrue
Jens Lekman|Night Falls Over Kortedala
No Age|Weirdo Rippers
Jay-Z|American Gangster
Deerhunter|Cryptograms
Justice|Cross
Lil Wayne|Da Drought 3
The National|Boxer
Kanye West|Graduation
Feist|The Reminder
Liars|Liars
Dirty Projectors|Rise Above
Okkervil River|The Stage Names
Studio|Yearbook 1
Dan Deacon|Spiderman of the Rings
The Tough Alliance|A New Chance (EP)
Various Artists|After Dark
Arcade Fire|Neon Bible
Dinosaur Jr.|Beyond
Bon Iver|For Emma, Forever Ago
Caribou|Andorra
Deerhoof|Friend Opportunity
Sally Shapiro|Disco Romance [listed as 2006 release]
King Khan & the Shrines|What Is?!
James Blackshaw|The Cloud of Unknowing
Black Lips|Good Bad Not Evil
Iron & Wine|The Shepherd's Dog
Grizzly Bear|Friend (EP)
Wu-Tang Clan|8 Diagrams
The White Stripes|Icky Thump
Beirut|The Flying Club Cup
Life Without Buildings|Live at the Annandale Hotel
Ghostface Killah|The Big Doe Rehab
Stars of the Lid|And Their Refinement of the Decline
Les Savy Fav|Let's Stay Friends
Ricardo Villalobos|Fabric 36
Marissa Nadler|Songs III: Bird on the Water
Yeasayer|All Hour Cymbals
Robert Wyatt|Comicopera
Dizzee Rascal|Maths + English
Tinariwen|Aman Iman [listed as 2006 release]"""
L[2008] = """Fleet Foxes|Fleet Foxes
Portishead|Third
No Age|Nouns
Cut Copy|In Ghost Colours
Deerhunter|Microcastle
TV on the Radio|Dear Science
Vampire Weekend|Vampire Weekend
M83|Saturdays = Youth
Hercules and Love Affair|Hercules and Love Affair
DJ /rupture|Uproot
Lil Wayne|Tha Carter III
Lindstrom|Where You Go I Go Too
Erykah Badu|New Amerykah Part One
Air France|No Way Down (EP)
Crystal Castles|Crystal Castles
Vivian Girls|Vivian Girls
Fucked Up|The Chemistry of Common Life
The Mae Shi|HLLLYH
The Walkmen|You & Me
Fuck Buttons|Street Horrrsing
Kanye West|808s & Heartbreak
Santogold|Santogold
Hot Chip|Made in the Dark
Gang Gang Dance|Saint Dymphna
Titus Andronicus|The Airing of Grievances
Atlas Sound|Let the Blind Lead Those Who Can See but Cannot Feel
Max Tundra|Parallax Error Beheads You
Flying Lotus|Los Angeles
The Hold Steady|Stay Positive
Los Campesinos!|Hold On Now, Youngster...
Fennesz|Black Sea
Nick Cave and the Bad Seeds|Dig, Lazarus, Dig!!!
Frightened Rabbit|The Midnight Organ Fight
Arthur Russell|Love Is Overtaking Me
Girl Talk|Feed the Animals
Wale|The Mixtape About Nothing
Grouper|Dragging a Dead Deer Up a Hill
The Bug|London Zoo
Times New Viking|Rip It Off
The Very Best|Esau Mwamwaya & Radioclit Are the Very Best
David Byrne & Brian Eno|Everything That Happens Will Happen Today
Bonnie 'Prince' Billy|Lie Down in the Light
Shearwater|Rook
Marnie Stern|This Is It and I Am It and You Are It...
Lykke Li|Youth Novels
Beach House|Devotion
The Tallest Man on Earth|Shallow Grave
High Places|High Places
Crystal Stilts|Alight of Night
Ponytail|Ice Cream Spiritual"""
L[2009] = """Animal Collective|Merriweather Post Pavilion
Dirty Projectors|Bitte Orca
The xx|xx
The Flaming Lips|Embryonic
Raekwon|Only Built 4 Cuban Linx... Pt. II
Grizzly Bear|Veckatimest
Bat for Lashes|Two Suns
Phoenix|Wolfgang Amadeus Phoenix
Fever Ray|Fever Ray
Girls|Album
Fuck Buttons|Tarot Sport
Yeah Yeah Yeahs|It's Blitz!
St. Vincent|Actor
Neon Indian|Psychic Chasms
Japandroids|Post-Nothing
Antony and the Johnsons|The Crying Light
The Very Best|Warm Heart of Africa
Atlas Sound|Logos
The Pains of Being Pure at Heart|The Pains of Being Pure at Heart
Real Estate|Real Estate
Neko Case|Middle Cyclone
Wild Beasts|Two Dancers
Memory Tapes|Seek Magic
Bill Callahan|Sometimes I Wish We Were an Eagle
DJ Quik & Kurupt|BlaQKout
Bon Iver|Blood Bank (EP)
Various Artists|5 Years of Hyperdub
Micachu and the Shapes|Jewellery
Yo La Tengo|Popular Songs
Royksopp|Junior
Sunn O)))|Monoliths & Dimensions
Bear in Heaven|Beast Rest Forth Mouth
Bibio|Ambivalence Avenue
Passion Pit|Manners
jj|jj n° 2
Dinosaur Jr.|Farm
The Antlers|Hospice
Major Lazer|Guns Don't Kill People... Lazers Do
Jim O'Rourke|The Visitor
Mos Def|The Ecstatic
Baroness|Blue Record
A Sunny Day in Glasgow|Ashes Grammar
Cymbals Eat Guitars|Why There Are Mountains
tUnE-yArDs|BiRd-BrAiNs
The Mountain Goats|The Life of the World to Come
Dan Deacon|Bromst
Zomby|Where Were U in '92?
DOOM|Born Like This
Cass McCombs|Catacombs
Woods|Songs of Shame"""
L[2010] = """Kanye West|My Beautiful Dark Twisted Fantasy
LCD Soundsystem|This Is Happening
Deerhunter|Halcyon Digest
Big Boi|Sir Lucius Left Foot: The Son of Chico Dusty
Beach House|Teen Dream
Vampire Weekend|Contra
Joanna Newsom|Have One on Me
James Blake|CMYK / Klavierwerke / The Bells Sketch (EPs)
Ariel Pink's Haunted Graffiti|Before Today
Titus Andronicus|The Monitor
Arcade Fire|The Suburbs
Janelle Monae|The ArchAndroid
No Age|Everything in Between
Flying Lotus|Cosmogramma
Robyn|Body Talk
Sleigh Bells|Treats
Caribou|Swim
Erykah Badu|New Amerykah Part Two
How to Dress Well|Love Remains
Oneohtrix Point Never|Returnal
The Walkmen|Lisbon
Girls|Broken Dreams Club (EP)
Das Racist|Sit Down, Man
Hot Chip|One Life Stand
Sufjan Stevens|The Age of Adz
Twin Shadow|Forget
Four Tet|There Is Love in You
The National|High Violet
The Fresh & Onlys|Play It Strange
The-Dream|Love King
Woods|At Echo Lake
Tyler, the Creator|Bastard
The Tallest Man on Earth|The Wild Hunt
Crystal Castles|Crystal Castles (II)
Gorillaz|Plastic Beach
Emeralds|Does It Look Like I'm Here?
Zola Jesus|Stridulum II
Rick Ross|Teflon Don
Best Coast|Crazy for You
Abe Vigoda|Crush
Delorean|Subiza
Drake|Thank Me Later
Tame Impala|Innerspeaker
Kylesa|Spiral Shadow
Gil Scott-Heron|I'm New Here
Matthew Dear|Black City
Women|Public Strain
Forest Swords|Dagger Paths
Wild Nothing|Gemini
Wavves|King of the Beach"""
L[2011] = """Bon Iver|Bon Iver, Bon Iver
Destroyer|Kaputt
M83|Hurry Up, We're Dreaming
PJ Harvey|Let England Shake
Girls|Father, Son, Holy Ghost
Oneohtrix Point Never|Replica
tUnE-yArDs|w h o k i l l
Drake|Take Care
Real Estate|Days
The Weeknd|House of Balloons
St. Vincent|Strange Mercy
James Blake|James Blake
EMA|Past Life Martyred Saints
Shabazz Palaces|Black Up
Fleet Foxes|Helplessness Blues
Kurt Vile|Smoke Ring for My Halo
Clams Casino|Instrumentals
Atlas Sound|Parallax
Danny Brown|XXX
Nicolas Jaar|Space Is Only Noise
Jay-Z & Kanye West|Watch the Throne
The Caretaker|An Empty Bliss Beyond This World
Bill Callahan|Apocalypse
Julianna Barwick|The Magic Place
Gang Gang Dance|Eye Contact
The Field|Looping State of Mind
Beyonce|4
Cut Copy|Zonoscope
DJ Quik|The Book of David
Tim Hecker|Ravedeath, 1972
Ty Segall|Goodbye Bread
Panda Bear|Tomboy
Fucked Up|David Comes to Life
Katy B|On a Mission
Frank Ocean|Nostalgia, Ultra
Kate Bush|50 Words for Snow
Iceage|New Brigade
Sandro Perri|Impossible Spaces
The War on Drugs|Slave Ambient
AraabMuzik|Electronic Dream
Liturgy|Aesthethica
SBTRKT|SBTRKT
Lykke Li|Wounded Rhymes
Colin Stetson|New History Warfare Vol. 2: Judges
Kendrick Lamar|Section.80
Cults|Cults
Sepalcure|Sepalcure
Toro y Moi|Underneath the Pine
Wild Flag|Wild Flag
Youth Lagoon|The Year of Hibernation"""

# Exclusions: EPs, mixtapes, compilations, DJ mixes, live/archival releases,
# and records listed as released in an earlier year. Ambiguous cases noted.
EXCLUDE = {
 (2006,"Dedication 2"):"mixtape",
 (2006,"LCD Soundsystem [listed as 2004 release]"):"listed as earlier-year release (verify: may be 45:33)",
 (2007,"Da Drought 3"):"mixtape",
 (2007,"Yearbook 1"):"compilation",
 (2007,"A New Chance (EP)"):"EP",
 (2007,"After Dark"):"compilation",
 (2007,"Disco Romance [listed as 2006 release]"):"earlier-year release",
 (2007,"Friend (EP)"):"EP",
 (2007,"Live at the Annandale Hotel"):"live/archival",
 (2007,"Fabric 36"):"DJ mix",
 (2007,"Aman Iman [listed as 2006 release]"):"earlier-year release",
 (2008,"Uproot"):"DJ mix",
 (2008,"No Way Down (EP)"):"EP",
 (2008,"Love Is Overtaking Me"):"archival compilation",
 (2008,"The Mixtape About Nothing"):"mixtape",
 (2008,"Esau Mwamwaya & Radioclit Are the Very Best"):"mixtape",
 (2009,"Blood Bank (EP)"):"EP",
 (2009,"5 Years of Hyperdub"):"compilation",
 (2010,"CMYK / Klavierwerke / The Bells Sketch (EPs)"):"EPs",
 (2010,"Broken Dreams Club (EP)"):"EP",
 (2010,"Sit Down, Man"):"mixtape",
 (2010,"Bastard"):"mixtape",
 (2011,"Instrumentals"):"mixtape",
 (2011,"Nostalgia, Ultra"):"mixtape",
}

rows=[]
for y,txt in L.items():
    lines=txt.strip().split("\n")
    assert len(lines)==50,(y,len(lines))
    for i,l in enumerate(lines,1):
        a,t=l.split("|")
        ex=EXCLUDE.get((y,t),"")
        rows.append(dict(year=y,rank=i,artist=a,title=t,band="top10" if i<=10 else "11-50",excluded=ex))
assert len([r for r in rows if r["excluded"]])==len(EXCLUDE)

SEED=20261111
rng=random.Random(SEED)
elig=[r for r in rows if not r["excluded"]]
top=[r for r in elig if r["band"]=="top10"]; low=[r for r in elig if r["band"]=="11-50"]
s_top=rng.sample(top,25); s_low=rng.sample(low,25)
for r in rows: r["sampled"]=""
for r in s_top+s_low: r["sampled"]="yes"
with open("output/pitchfork_frame_2006_2011.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("frame",len(rows),"eligible",len(elig),"top10 elig",len(top),"11-50 elig",len(low))
samp=sorted(s_top+s_low,key=lambda r:(r["year"],r["rank"]))
for r in samp: print(f'{r["year"]}|{r["rank"]}|{r["artist"]}|{r["title"]}')
from collections import Counter
print(Counter(r["year"] for r in samp))
