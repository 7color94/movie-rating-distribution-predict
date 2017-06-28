Pre-release Movie Rating Distribution Predict
---

This project is a extremely complete implementation of paper 《Pre-release Prediction of Crowd Opinion on Movies by Label Distribution Learning. IJCAI. 2015》.

### Data

All training and testing Data are crawled from IMDb.com, reference to `ldsvr/oldmoviecrawler.py` and `ldsvr/newmoviecrawler.py` for details.

How can I crawl movie data from IMDb? Just reference to:

- [IMDB电影数据库](http://sukai.me/imdb-movies-crawl/)
- [IMDB数据库结构](http://sukai.me/imdb-db-structure/)

### Feature Processing and Selection

Having training movies and testing movies, we need to process and select features from these data, as the paper said.

Reference to `ldsvr/features_counting.py`, `ldsvr/features_indexing.py`, `ldsvr/matrix_persistent.py`, `ldsvr/test_matrix.py` and `ldsvr/training_matrix.py` for details. And I use Redis DB for convenient feature counting and processing.

This process can form training matrix and testing matrix for LDSVR Algorithm.

### Train

Following the algorithm from paper, I use LDSVR Algorithm to train the model. Please reference to `ldsvr/ldsvr.py` and [paper](http://cse.seu.edu.cn/PersonalPage/xgeng/LDL/resource/ijcai15.pdf) for details. 

### Results

I use Tornado to show results. Here are some website snapshots shown below. And the website need mysql DB for data support.

![](https://raw.githubusercontent.com/7color94/movie-rating-distribution-predict/master/results/index_pic.png)

![](https://raw.githubusercontent.com/7color94/movie-rating-distribution-predict/master/results/movie_detail_pic.png)

![](https://raw.githubusercontent.com/7color94/movie-rating-distribution-predict/master/results/movie_rating_pic1.png)

![](https://raw.githubusercontent.com/7color94/movie-rating-distribution-predict/master/results/movie_rating_pic2.png)

### References

- [Geng, Xin, and Peng Hou. "Pre-release Prediction of Crowd Opinion on Movies by Label Distribution Learning." IJCAI. 2015.](http://cse.seu.edu.cn/PersonalPage/xgeng/LDL/resource/ijcai15.pdf)
- [IMDb](http://www.imdb.com/)
- [Tornado](http://www.tornadoweb.org/en/stable/#)
- [Redis](https://redis.io/)
- [Readfree.me](http://readfree.me/)
