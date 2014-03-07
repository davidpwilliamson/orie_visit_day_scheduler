import csv
import sys
import visit_day_scheduler


offices = {
   # actual professors
   "Bindel David" : "425 Gates",
   "Birman Ken" : "435 Gates",
   "Bala Kavita": "315 Gates",
   "Cardie Claire" : "417 Gates",
   "Chen Tsuhan" : "304 Rhodes",
   "Choudhury Tanzeem" : "243 Gates",
   "Constable Bob" : "320 Gates",
   "Cosley Dan" : "244 Gates",
   "Edelman Shimon" : "405 Gates",
   "Foster Nate" : "432 Gates",
   "Ghosh Arpita": "207 Gates",
   "Gomes Carla" : "353 Gates",
   "Halpern Joe" : "402A Gates",
   "Hirsch Haym" : "105 Gates",
   "Hopcroft John" : "426 Gates",
   "James Doug" : "311 Gates",
   "Joachims Thorsten" : "418 Gates",
   "Kleinberg Bobby" : "317 Gates",
   "Kleinberg Jon" : "318 Gates",
   "Kozen Dexter" : "436 Gates",
   "Lee Lillian" : "419 Gates",
   "Lipson Hod" : "239 Upson (Robo lab)",
   "Marschner Steve" : "313 Gates",
   "Martinez Jose" : "336 Rhodes",
   "Mimno David" : "205 Gates",
   "Myers Andrew" : "428 Gates",
   "Saxena Ashutosh" : "321 Gates",
   "Selman Bart" : "351 Gates",
   "Senges Phoebe" : "210 Gates",
   "Shmoys David" : "310 Gates",
   "Siepel Adam" : "102E Weill",
   "Sirer Gun" : "438 Gates",
   "Steurer David": "319 Gates",
   "Strogatz Steven" : "533 Gates",
   "Tardos Eva" : "316 Gates",
   "Tate Ross" : "434 Gates",
   "Van Renesse Robbert" : "433 Gates",
   "Weatherspoon Hakim" : "427 Gates",
   "Williamson David" : "225 Gates",
   "Easley David" : "450 Uris",
   "Frazier Peter" : "232 Rhodes",
   "Blume Lawrence" : "430 Uris",

  # students
  "Magrino Tom" : "440B Gates",
  "O'Mahony Eoin" : "302 Gates",
  "Shi Jonathan" : "305 Gates",
  "Reitblatt Mark" : "442 Gates",
  "Milano Matthew" : "440 Gates",
"Jalaly Pooya" : "336 Gates",
  "Leung Samantha" : "322 Gates",
    "Ghose Saugata" : "356 Upson",
  "Wehrwein Scott" : "345 Gates",
  "Gkountouvas Theo" : "305 Gates",
  "Shen Zhiming" : "407 Gates",
  "Hirsch Andrew" : "407 Gates",
  "Nkounkou Brittany" : "302 Gates",
  "Sipos Ruben" : "349 Gates",
  "Jia Qin" : "440 Gates",
  "Rotabi Rahmtin" : "301 Gates",
  "Passi Samir" : "",
  "Hopkins Sam" : "401 Gates",
  "Muehlboeck Fabian" : "401 Gates",
  "Thompson Laure" : "407 Gates",
  "DiLorenzo Jonathan" : "305 Gates",
  "Misra Dipendra" : "301 Gates",
  "Sung Jaeyong" : "350 Gates",
  "Wang Lu" : "413 Gates",
  "Park Jon" : "349 Gates",
  "Arden Owen" : "456 Gates",
  "Smolka Steffen" : "407 Gates",
  "Li Erluo" : "440 Gates",

  # WIC meeting
  "WIC1a" : "Meet in Gates Lounge",
  "WIC1b" : "Meet in Gates Lounge",
  "WIC1c": "Meet in Gates Lounge",
  "WIC1d": "Meet in Gates Lounge",
  "WIC1e": "Meet in Gates Lounge",
  "WIC1f": "Meet in Gates Lounge",
  "WIC2a": "Meet in Gates Lounge",
  "WIC2b": "Meet in Gates Lounge",
  "WIC2c": "Meet in Gates Lounge",
  "WIC2d": "Meet in Gates Lounge",
  "WIC2e": "Meet in Gates Lounge",
  "WIC2f": "Meet in Gates Lounge",

  # break
  "" : ""
}


def main():
  master = open(sys.argv[1], 'rb')
  masterreader = csv.reader(master)
  for r in masterreader:
    if not r[0] == "Visitor": # dump the first line
      print r[0]
      outfile = open(r[0].split(" ")[1] + '.tex', 'wb')
      outstring = r"""\documentclass{article}
% Load packages
\usepackage{amsmath}
\usepackage{amsthm}
\usepackage{amssymb}
\usepackage{amsfonts}
\usepackage{sectsty}
\usepackage{titling}
\usepackage{fancyhdr}
\usepackage{enumitem}
\usepackage[top=1.25in, bottom=1.25in, left=1.3in, right=1.3in]{geometry}
\usepackage{complexity}
\usepackage{algpseudocode}
\usepackage{algorithm}

% Make sexy marginalia
\let\oldmarginpar\marginpar
\renewcommand\marginpar[1]{\-\oldmarginpar[\raggedleft\footnotesize #1]%
{\raggedright\footnotesize #1}}

% Set up the title block
\pretitle{\begin{center} \Large \scshape} 
\posttitle{\vskip 0.4em \hrule \end{center}}
\preauthor{\begin{center} \large}
\postauthor{\end{center}}
\predate{\begin{center}}
\postdate{\end{center}}

% Set up headers
\lhead{\scshape \theauthor}
\rhead{\scshape \rightmark}
\pagestyle{fancy}
  
% Set margin and allow user control over spacing
% \usepackage{setspace}
% \usepackage[margin=1.25in]{geometry}

\usepackage{setspace}
\usepackage{color}
\usepackage[bookmarks=true]{hyperref}

\title{Schedule For """ + r[0] +r"""}
\author{Cornell Computer Science}
\date{Prospective PhD Visit Day}
\fancyheadoffset[LE,RO]{0pt}{\marginparsep + \marginparwidth}
\begin{document}
\maketitle

\section*{Monday, March 10}

\begin{tabular}{l l l}
  8:30 -- 9:30 & Breakfast and Welcome & TBA\\
  9:40 -- 10:00 &""" +  r[1] + "&" + offices[r[1]] + r"""\\
 10:05 -- 10:25 &""" +  r[2] + "&" + offices[r[2]]  + r"""\\
 10:30 -- 10:50 &""" +  r[3] + "&" + offices[r[3]]  + r"""\\
 11:00 -- 11:20 &""" +  r[4] + "&" + offices[r[4]]  + r"""\\
 11:25 -- 11:45 &""" +  r[5] + "&" + offices[r[5]]  + r"""\\
  11:45 -- 2:00 & Area Lunches & Various (see online) \\
   2:00 -- 3:00 & Student Panel & Gates 310 \\
   3:00 -- 3:20 & """ +  r[6] + "&" + offices[r[6]]  + r"""\\
   3:25 -- 3:45 & """ +  r[7] + "&" + offices[r[7]]  + r"""\\
   3:50 -- 4:10 & """ +  r[8] + "&" + offices[r[8]]  + r"""\\
   4:15 -- 4:35 & """ +  r[9] + "&" + offices[r[9]]  + r"""\\
   4:40 -- 5:00 & """ +  r[10] + "&" + offices[r[10]]  + r"""\\
   5:00 -- 6:00 & Break & \\
           6:15 & Leave for Dinner Downton & Meet in Gates Lounge\\
  8:30 -- 10:30 & Party -- Dessert and Drinks & Gates Atrium \\
  10:30 -- bedtime & Board games, Bars & Leaving from Gates Atrium \\
\end{tabular}

\section*{Tuesday, March 11}
\begin{tabular}{l l l}
  10:00 -- 11:00 & Brunch & Statler Hotel \\
   11:00 -- 1:00 & Lab Open Houses (see online), 1-on-1 meetings (see below)\\
  11:00 -- 11:20 & """ +  r[11] + "&" + offices[r[11]]  + r"""\\
  11:25 -- 11:45 & """ +  r[12] + "&" + offices[r[12]]  + r"""\\
  11:50 -- 12:10 & """ +  r[13] + "&" + offices[r[13]]  + r"""\\
  12:15 -- 12:35 & """ +  r[14] + "&" + offices[r[14]]  + r"""\\
   12:40 -- 1:00 & """ +  r[15] + "&" + offices[r[15]]  + r"""\\
    1:00 -- 2:30 & Lunch in Collegetown & Meet in Gates Lounge\\
    2:30 -- 6:00 & Explore Campus and Ithaca & \\
    6:00 -- 6:30 & Break \\
    6:30 -- 8:00 & Dinner in Collegetown & Meet in Gates Lounge\\
 8:00 -- bedtime & Party at Ross Tate's house & Meet in Gates Lounge
\end{tabular}


\end{document}"""
      outfile.write(outstring)
      outfile.close()

if __name__ == "__main__":
  main()

