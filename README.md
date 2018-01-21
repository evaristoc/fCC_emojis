# freeCodeCamp Main Chatroom Emoji Project

This repository contains part of the code and datasets that were used for the medium article [The Emoji developers use most](https://medium.freecodecamp.org/and-the-most-popular-developer-emoji-is-d660a9687be7).

I used Python and the Gitter API to get the messages from the freeCodeCamp main chat room. Python libraries like `multiprocessing` and `emoji` were used to transform the data. Part of the transformations also required data available online, for which I made customized scrapers also with Python libraries (`requests`, `urllib`, `BeautifulSoup4`). To analyze the data I used plain Python and some `pandas`. Explorative visualizations were made using `matplotlib` while the interactive ones where made in `D3.js`.

d3.js visualizations can be found at:
* [The beeswarm](https://bl.ocks.org/evaristoc/d5531fb65c599370f777370e44f14242)
* [The billboard](http://bl.ocks.org/evaristoc/663eca9722c37bd7c0d254edfb0c9d00)

Regarding the raw datasets used for this project they are now available on the [freeCodeCamp’s Kaggle account](https://www.kaggle.com/free-code-camp/all-posts-public-main-chatroom).

The motivation of this project adheres to the mission of the [freeCodeCamp’s Open Data Initiative](https://github.com/freeCodeCamp/open-data). A big thanks to the people in the freeCodeCamp DataScience room and specially to [mstellaluna](https://github.com/mstellaluna) in helping with this project. 
