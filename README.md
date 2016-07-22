# sfm-wayback

This is an experiment with providing access to archived social media data recorded from social media APIs. 
In particular, it plugs into the [Social Feed Manager](go.gwu.edu/sfm) (SFM) infrastructure and uses [PyWB](https://github.com/ikreymer/pywb)
(an implementation of wayback software for web archives) to serve social media data and related web resources recorded 
in WARC files by SFM harvesters.

sfm-wayback can be used on conjunction with [sfm-wayback-viewer](https://github.com/gwu-libraries/sfm-wayback), 
an experimental web application which uses the data served by PyWB and provides a rendering of the social media data 
(which is in JSON).

sfm-wayback is realized as two Docker containers.  The first runs PyWB.  The second listens for WARC 
created messages published by SFM harvesters and indexes the WARC files in PyWB.

## Running sfm-wayback
1. Clone this project.
2. Copy `example.docker-compose.yml` to `docker-compose.yml` and `example.env` to `.env`.
3. Bring up SFM with `docker-compose up -d`. This will take a few minutes.
4. Collect some social media data and related web resources. For more information on using SFM see the [user
guide](http://sfm.readthedocs.io/en/latest/quickstart.html).  SFM UI will be available at 
[http://<your server>:8080/ui/](http://localhost:8080/ui/).

The PyWB search page will be available at [http://<your server>:8081/sfm](http://localhost:8081/sfm).
As an example, to get a list of the archived Twitter REST API calls go to 
[http://<your server>:8081/sfm/*/https://api.twitter.com/1.1/*](http://localhost:8081/sfm/*/https://api.twitter.com/1.1/*).

For more information on installing SFM, see the [installation and configuration](http://sfm.readthedocs.io/en/latest/install.html) docs.

## Limitations
**This is only an experiment.**