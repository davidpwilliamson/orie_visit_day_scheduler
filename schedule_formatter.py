import csv
import sys
import visit_day_scheduler


offices = {
   # actual professors

   "Bland Bob" : "Rhodes 233",
   "Dai Jim" : "Rhodes 226",
   "Frazier Peter" : "Rhodes 232",
   "Henderson Shane" : "Rhodes 230",
   "Iyer Kris" : "Rhodes 225",
   "Jackson Peter" : "Rhodes 218",
   "Lewis Adrian" : "Rhodes 234",
   "Lewis Mark" : "Rhodes 221",
   "Minca Andreea" : "Rhodes 222",
   "Patie Pierre" : "Rhodes 219",
   "Pender Jamol" : "",
   "Renegar Jim" : "Rhodes 224",
   "Resnick Sid" : "Rhodes 284",
   "Ruppert David" : "Rhodes 238",
   "Samorodnitsky Gena" : "Rhodes 220",
   "Shmoys David" : "Rhodes 214",
   "Shoemaker Chris" : "",
   "Tardos Eva" : "",
   "Todd Mike" : "Rhodes 229",
   "Topaloglu Huseyin" : "Rhodes 223",
   "Trotter Les" : "Rhodes 235",
   "Williamson David" : "Rhodes 236",
   "Woodard Dawn" : "Rhodes 228"

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

