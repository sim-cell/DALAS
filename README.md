# Projet DALAS

Sujet général : 
  La Pollution et les Effets de la Mode Ephémère (Fast Fashion) sur l'Environnement et les Humains

Au début, notre seul axe était de se concentrer sur le changement de climat mais désormais, on a décidé d'entrer en détail sur les sujets concernant la mode éphémère.
Pourquoi? : 
Le secteur de textile est un des secteurs les plus polluants du monde. L'un des stratégies de ce secteur est la sur-production de leur biens car même s'il y a des nombreux produits réstants, il y a aussi du profit.

Donc le but de notre projet est de voir le changement du climat jusqu'aujourd'hui, la qualité de vie des pays courants

Afin de voir les effets et les raisons de la mode éphémère on a plusieurs axes:
- Comment ont varié les paramètres d'environnement dans 10 ans ? Avec régréssion peut-on éstimer l'avenir?
  Cela est notre observation de la base. Au cours des années on veut voir la variance de la pollution et la qualiré de vie selon les pays.
- H&M est un des pioniers de ce secteur, quels textiles utilisent-ils dans leurs vêtements ?
  En scrapant des vêtements dans leur site, on peut voir leurs prix, la composition des matériaux etc.
- Fast fashion est il profitable ? 
- En regardant les informations courantes sur les problèmes environnementaux dans des pays différents, on peut observer les effets de la sur-production. Comment les pays sont affectés? Est-ce qu'il y a un lien entre les pays où il y a beaucoup de production?
- Quels sont les problèmes avec fast fashion?
  - Polyester => trop utilisé et synthétique. CO2, pollution de l'aire, non-biodégradable, micro-plastiques causent la pollution marine etc.
  - Cotton => nécessite de grandes quantités d'eau
  - On peut utiliser ces effets sur les données scrappés afin de calculer le dommage total.

- Questions un peu plus détaillées:
    - Les projets environnementaux et les pays participants. On peut les scraper d'ici : https://open.unep.org/

     
Data :
Déjà scrapé :
- Les données entre 2014-2024 sont dans un tableau qu'on scrape. (/data/data_annees.csv)
- Les données plus détaillés pour chaque pays (/data/data_pollution.csv)

En cours de scraping:
- Les produits de HM. On a les liens des produits scrapé du site mais on n'a pas encore scrapé les informations. On utilise HM USA car HM France avait le pire html possible.

A scraper : 
- PROBABLY ILLEGAL Profits HM (facile à scraper): https://hmgroup.com/investors/five-year-summary/ 


Data Prêt:
- CO2 emission par secteur/pays :
https://climatedata.imf.org/pages/greenhouse-gas-emissions#gg4 
(/data/Direct_Investment-related_Indicators.csv)
Il faut faire de nettoyage quand même car il y a tous les autres secteurs dedans. 
- H&M prix historique mais je suis nulle en finance donc je n'ai aucune idée : https://finance.yahoo.com/quote/HM-B.ST/history?period1=946857600&period2=1708732800&interval=1mo&filter=history&frequency=1mo&includeAdjustedClose=true
(/data/HM-B.ST.csv)

Data téléchargeable si nécessaire :
- PLusieurs data sur plastique etc : https://ourworldindata.org/plastic-pollution#explore-data-on-plastic-pollution
__________________________________________________________
15.02.2024
- les données qu'on a entre 2014-2024 :
  - les pays
  - indice climatique
  -  cout de la vie
  -  indice de pollution
  -  qualité de vie
-données détaillés sur :
  - pollution => de l'eau, de l'aire
  - traffic => indice d'emission de CO2, mpyenne d'utilisation des transports publiques/vélos etc.
    
- quality of life vs pollution
- cost of living vs pollution
  on a accès aux différents types de pollution : 
    - Air Pollution et Air quality
    - Drinking Water Pollution and Inaccessibility
      
regression : 
  how do some values varied over the year, what is the extimation for the next year to come?
classification :
  les pays pollué
  par exemple on a Isle of man où il n'y a vraiment pas de pollution et en Nigeria.
_____________________________________________________________________________________
