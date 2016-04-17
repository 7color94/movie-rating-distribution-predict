#!/usr/bin/env python
# -*- coding: utf-8 -*-

class newMovie(object):

    def __init__(self):
        self._id = 0
        self._title = ''
        self._color = ''
        self._genre = ''
        self._language = ''
        self._soundmix = ''
        self._country = ''
        self._cast = ''
        self._producer = ''
        self._writer = ''
        self._cinematographer = ''
        self._composer = ''
        self._costume_designer = ''
        self._director = ''
        self._editor = ''
        self._company = ''
        self._year = 0
        self._running_time = 0
        self._keywords = ''
        self._imdb_url = ''
        self._poster_url = ''

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def soundmix(self):
        return self._soundmix

    @soundmix.setter
    def soundmix(self, value):
        self._soundmix = value

    @property
    def cinematographer(self):
        return self._cinematographer

    @cinematographer.setter
    def cinematographer(self, value):
        self._cinematographer = value

    @property
    def composer(self):
        return self._composer

    @composer.setter
    def composer(self, value):
        self._composer = value

    @property
    def costume_designer(self):
        return self._costume_designer

    @costume_designer.setter
    def costume_designer(self, value):
        self._costume_designer = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        self._year = value

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, value):
        self._country = value

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, value):
        self._language = value

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, value):
        self._keywords = value

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, value):
        self._genre = value

    @property
    def cast(self):
        return self._cast

    @cast.setter
    def cast(self, value):
        self._cast = value

    @property
    def editor(self):
        return self._editor

    @editor.setter
    def editor(self, value):
        self._editor = value

    @property
    def writer(self):
        return self._writer

    @writer.setter
    def writer(self, value):
        self._writer = value

    @property
    def company(self):
        return self._company

    @company.setter
    def company(self, value):
        self._company = value

    @property
    def director(self):
        return self._director

    @director.setter
    def director(self, value):
        self._director = value

    @property
    def producer(self):
        return self._producer

    @producer.setter
    def producer(self, value):
        self._producer = value

    @property
    def running_time(self):
        return self._running_time

    @running_time.setter
    def running_time(self, value):
        self._running_time = value

    @property
    def imdb_url(self):
        return self._imdb_url

    @imdb_url.setter
    def imdb_url(self, value):
        self._imdb_url = value

    @property
    def poster_url(self):
        return self._poster_url

    @poster_url.setter
    def poster_url(self, value):
        self._poster_url = value


class oldMovie(object):

    def __init__(self):
        self._id = 0
        self._title = ''
        self._year = 0

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        self._year = value


class votesMovie(object):

    def __init__(self):
        self._id = 0
        self._title = ''
        self._year = 0
        self._rating = 0.0
        self._votes = 0
        self._votes_one = 0
        self._votes_two = 0
        self._votes_three = 0
        self._votes_four = 0
        self._votes_five = 0
        self._votes_six = 0
        self._votes_seven = 0
        self._votes_eight = 0
        self._votes_nine = 0
        self._votes_ten = 0
        self._votes_males = 0
        self._rating_males = 0.0
        self._votes_females = 0
        self._rating_females = 0.0
        self._votes_aged_under_eighteen = 0
        self._rating_aged_under_eighteen = 0.0
        self._votes_males_under_eighteen = 0
        self._rating_males_under_eighteen = 0.0
        self._votes_females_under_eighteen = 0
        self._rating_females_under_eighteen = 0.0
        self._votes_aged_eighteen_twentyNine = 0
        self._rating_aged_eighteen_twentyNine = 0.0
        self._votes_males_eighteen_twentyNine = 0
        self._rating_males_eighteen_twentyNine = 0.0
        self._votes_females_eighteen_twentyNine = 0
        self._rating_females_eighteen_twentyNine = 0.0
        self._votes_aged_thirty_fourtyFour = 0
        self._rating_aged_thirty_fourtyFour = 0.0
        self._votes_males_thirty_fourtyFour = 0
        self._rating_males_thirty_fourtyFour = 0.0
        self._votes_females_thirty_fourtyFour = 0
        self._rating_females_thirty_fourtyFour = 0.0
        self._votes_aged_fourtyFive = 0
        self._rating_aged_fourtyFive = 0.0
        self._votes_males_fourtyFive = 0
        self._rating_males_fourtyFive = 0.0
        self._votes_females_fourtyFive = 0
        self._rating_females_fourtyFive = 0.0
        self._votes_imdb_staff = 0
        self._rating_imdb_staff = 0.0
        self._votes_top_thousand_voters = 0
        self._rating_top_thousand_voters = 0.0
        self._votes_us_users = 0
        self._rating_us_users = 0.0
        self._votes_nous_users = 0
        self._rating_nous_users = 0.0

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        self._year = value

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        self._rating = value

    @property
    def votes(self):
        return self._votes

    @votes.setter
    def votes(self, value):
        self._votes = value

    @property
    def votes_one(self):
        return self._votes_one

    @votes_one.setter
    def votes_one(self, value):
        self._votes_one = value

    @property
    def votes_two(self):
        return self._votes_two

    @votes_two.setter
    def votes_two(self, value):
        self._votes_two = value

    @property
    def votes_three(self):
        return self._votes_three

    @votes_three.setter
    def votes_three(self, value):
        self._votes_three = value

    @property
    def votes_four(self):
        return self._votes_four

    @votes_four.setter
    def votes_four(self, value):
        self._votes_four = value

    @property
    def votes_five(self):
        return self._votes_five

    @votes_five.setter
    def votes_five(self, value):
        self._votes_five = value

    @property
    def votes_six(self):
        return self._votes_six

    @votes_six.setter
    def votes_six(self, value):
        self._votes_six = value

    @property
    def votes_seven(self):
        return self._votes_seven

    @votes_seven.setter
    def votes_seven(self, value):
        self._votes_seven = value

    @property
    def votes_eight(self):
        return self._votes_eight

    @votes_eight.setter
    def votes_eight(self, value):
        self._votes_eight = value

    @property
    def votes_nine(self):
        return self._votes_nine

    @votes_nine.setter
    def votes_nine(self, value):
        self._votes_nine = value

    @property
    def votes_ten(self):
        return self._votes_ten

    @votes_ten.setter
    def votes_ten(self, value):
        self._votes_ten = value

    @property
    def votes_males(self):
        return self._votes_males

    @votes_males.setter
    def votes_males(self, value):
        self._votes_males = value

    @property
    def rating_males(self):
        return self._rating_males

    @rating_males.setter
    def rating_males(self, value):
        self._rating_males = value

    @property
    def votes_females(self):
        return self._votes_females

    @votes_females.setter
    def votes_females(self, value):
        self._votes_females = value

    @property
    def rating_females(self):
        return self._rating_females

    @votes_females.setter
    def rating_females(self, value):
        self._rating_females = value

    @property
    def votes_aged_under_eighteen(self):
        return self._votes_aged_under_eighteen

    @votes_aged_under_eighteen.setter
    def votes_aged_under_eighteen(self, value):
        self._votes_aged_under_eighteen = value

    @property
    def rating_aged_under_eighteen(self):
        return self._rating_aged_under_eighteen

    @rating_aged_under_eighteen.setter
    def rating_aged_under_eighteen(self, value):
        self._rating_aged_under_eighteen = value

    @property
    def votes_males_under_eighteen(self):
        return self._votes_males_under_eighteen

    @votes_males_under_eighteen.setter
    def votes_males_under_eighteen(self, value):
        self._voes_males_under_eighteen = value

    @property
    def rating_males_under_eighteen(self):
        return self._rating_males_under_eighteen

    @rating_males_under_eighteen.setter
    def rating_males_under_eighteen(self, value):
        self._rating_males_under_eighteen = value

    @property
    def votes_females_under_eighteen(self):
        return self._votes_females_under_eighteen

    @votes_females_under_eighteen.setter
    def votes_females_under_eighteen(self, value):
        self._votes_females_under_eighteen = value

    @property
    def rating_females_under_eighteen(self):
        return self._rating_females_under_eighteen

    @rating_females_under_eighteen.setter
    def rating_females_under_eighteen(self, value):
        self._rating_females_under_eighteen = value

    @property
    def votes_aged_eighteen_twentyNine(self):
        return self._votes_aged_eighteen_twentyNine

    @votes_aged_eighteen_twentyNine.setter
    def votes_aged_eighteen_twentyNine(self, value):
        self._votes_aged_eighteen_twentyNine

    @property
    def rating_aged_eighteen_twentyNine(self):
        return self._rating_aged_eighteen_twentyNine

    @rating_aged_eighteen_twentyNine.setter
    def rating_aged_eighteen_twentyNine(self, value):
        self._rating_aged_eighteen_twentyNine = value

    @property
    def votes_males_eighteen_twentyNine(self):
        return self._votes_males_eighteen_twentyNine

    @votes_males_eighteen_twentyNine.setter
    def votes_males_eighteen_twentyNine(self, value):
        self._votes_males_eighteen_twentyNine = value

    @property
    def rating_males_eighteen_twentyNine(self):
        return self._rating_males_eighteen_twentyNine

    @rating_males_eighteen_twentyNine.setter
    def rating_males_eighteen_twentyNine(self, value):
        self._rating_males_eighteen_twentyNine = value

    @property
    def votes_females_eighteen_twentyNine(self):
        return self._votes_females_eighteen_twentyNine

    @votes_females_eighteen_twentyNine.setter
    def votes_females_eighteen_twentyNine(self, value):
        self._votes_females_eighteen_tewntyNine = value

    @property
    def rating_females_eighteen_twentyNine(self):
        return self._rating_females_eighteen_twentyNine

    @rating_females_eighteen_twentyNine.setter
    def rating_females_eighteen_twentyNine(self, value):
        self._rating_females_eighteen_twentyNine = value

    @property
    def votes_aged_thirty_fourtyFour(self):
        return self._votes_aged_thirty_fourtyFour

    @votes_aged_thirty_fourtyFour.setter
    def votes_aged_thirty_fourtyFour(self, value):
        self._votes_aged_thirty_fourtyFour = value

    @property
    def rating_aged_thirty_fourtyFour(self):
        return self._rating_aged_thirty_fourtyFour

    @rating_aged_thirty_fourtyFour.setter
    def rating_aged_thirty_fourtyFour(self, value):
        self._rating_aged_thirty_fourtyFour = value

    @property
    def votes_males_thirty_fourtyFour(self):
        return self._votes_males_thirty_fourtyFour

    @votes_males_thirty_fourtyFour.setter
    def votes_males_thirty_fourtyFour(self, value):
        self._votes_males_thirty_fourtyFour = value

    @property
    def rating_males_thirty_fourtyFour(self):
        return self._rating_males_thirty_fourtyFour

    @rating_males_thirty_fourtyFour.setter
    def rating_males_thirty_fourtyFour(self, value):
        self._rating_males_thirty_fourtyFour = value

    @property
    def votes_females_thirty_fourtyFour(self):
        return self._votes_females_thirty_fourtyFour

    @votes_females_thirty_fourtyFour.setter
    def votes_females_thirty_fourtyFour(self, value):
        self._votes_femals_thirty_fourtyFour = value

    @property
    def rating_females_thirty_fourtyFour(self):
        return self._rating_females_thirty_fourtyFour

    @rating_females_thirty_fourtyFour.setter
    def rating_females_thirty_fourtyFour(self, value):
        self._rating_females_thirty_fourtyFour = value

    @property
    def votes_aged_fourtyFive(self):
        return self._votes_aged_fourtyFive

    @votes_aged_fourtyFive.setter
    def votes_aged_fourtyFive(self, value):
        self._votes_aged_fourtyFive = value

    @property
    def rating_aged_fourtyFive(self):
        return self._rating_aged_fourtyFive

    @rating_aged_fourtyFive.setter
    def rating_aged_fourtyFive(self, value):
        self._rating_aged_fourtyFive = value

    @property
    def votes_males_fourtyFive(self):
        return self._votes_males_fourtyFive

    @votes_males_fourtyFive.setter
    def votes_males_fourtyFive(self, value):
        self._votes_males_fourtyFive = value

    @property
    def rating_males_fourtyFive(self):
        return self._rating_males_fourtyFive

    @rating_males_fourtyFive.setter
    def rating_males_fourtyFive(self, value):
        self._rating_males_fourtyFive = value

    @property
    def votes_females_fourtyFive(self):
        return self._votes_females_fourtyFive

    @votes_females_fourtyFive.setter
    def votes_females_fourtyFive(self, value):
        self._votes_females_fourtyFive = value

    @property
    def rating_females_fourtyFive(self):
        return self._rating_females_fourtyFive

    @rating_females_fourtyFive.setter
    def rating_females_fourtyFive(self, value):
        self._rating_females_fourtyFive = value

    @property
    def votes_imdb_staff(self):
        return self._votes_imdb_staff

    @votes_imdb_staff.setter
    def votes_imdb_staff(self, value):
        self._votes_imdb_stdff = value

    @property
    def rating_imdb_staff(self):
        return self._rating_imdb_staff

    @rating_imdb_staff.setter
    def rating_imdb_staff(self, value):
        self._rating_imdb_staff = value

    @property
    def votes_top_thousand_voters(self):
        return self._votes_top_thousand_voters

    @votes_top_thousand_voters.setter
    def votes_top_thousand_voters(self, value):
        self._votes_top_thousand_voters = value

    @property
    def rating_votes_top_thousand_voters(self):
        return self._rating_votes_top_thousand_voters

    @rating_votes_top_thousand_voters.setter
    def rating_votes_top_thousands_voters(self, value):
        self._rating_votes_top_thousands_voters = value

    @property
    def votes_us_users(self):
        return self._votes_us_users

    @votes_us_users.setter
    def votes_us_users(self, value):
        self._votes_us_users = value

    @property
    def rating_us_users(self):
        return self._rating_us_users

    @rating_us_users.setter
    def rating_us_users(self, value):
        self._rating_us_users = value

    @property
    def votes_nous_users(self):
        return self._votes_nous_users

    @votes_nous_users.setter
    def votes_nous_users(self, value):
        self._votes_nous_users = value

    @property
    def rating_nous_users(self):
        return self._rating_nous_users

    @rating_nous_users.setter
    def rating_nous_users(self, value):
        self._rating_nous_users = value