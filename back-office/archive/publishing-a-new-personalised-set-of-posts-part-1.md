# How I'm Building Personalised News Feeds with Semantic Graphs - Part 1

> Recovered from mvp.myfeeds.ai, published 26 Mar 2025: Following the technical explanation of how I'm building the Semantic Knowledge Graphs and Establishing Provenance, let's look at the current (MVP) process of publishing a new set of…

*Source: <https://myfeeds.sgit.ai/back-office/archive/publishing-a-new-personalised-set-of-posts-part-1.html> · site v0.1.7 · this file is generated from the same content as
the page, so the two cannot drift. Every page on this site has a `.md` twin; internal
links below point at them.*

---

Recovered from the archive

# How I'm Building Personalised News Feeds with Semantic Graphs - Part 1

**Originally**

: `https://mvp.myfeeds.ai/publishing-a-new-personalised-set-of-posts-part-1/` — the site no longer exists

**Published**

: 26 Mar 2025

**Author**

: Dinis Cruz

**Tags**

: How it works

**Recovered**

: From a capture of the site's RSS feed, which carried the full body. The markdown is at `back-office/archive/mvp.myfeeds.ai__posts/publishing-a-new-personalised-set-of-posts-part-1.md`.

This is recovered content, reproduced as it was published. Its links point at pages that in many cases no longer resolve and are left exactly as written. Its **images are served from this repository** — the originals were recovered from the same archive as the text, and each one carries the URL it came from in its title attribute, so the reference is rewritten and recorded rather than rewritten and hidden. An image the archive did not capture is marked as missing rather than left broken.

↓ recovered article begins 26 Mar 2025 · Dinis Cruz

[image not recovered: `feed-timeline.mgraph--4-.png`]

Following the technical explanation of how I'm building the [Semantic Knowledge Graphs](https://mvp.myfeeds.ai/building-semantic-knowledge-graphs-with-llms-inside-myfeeds-ais-multi-phase-architecture/) and [Establishing Provenance](https://mvp.myfeeds.ai/establishing-provenance-and-deterministic-behaviour-in-an-llm-powered-news-feed-first-myfeeds-mvp/), let's look at the current (MVP) process of publishing a new set of personalised posts for multiple personas (CEO, CISO, CTO, and Board Members).

The whole process is managed via a FastAPI service running on a serverless function (in this case AWS Lambda)

I'm using the [OSBot-Fast-API](https://github.com/owasp-sbot/OSBot-Fast-API?ref=mvp.myfeeds.ai) open source package, which makes it super easy to create these serverless functions (easier than using FastAPI directly)

Here are the default methods that are added when you create and deploy an OSBot-Fast-API project

[image · `image-50.png`](../../back-office/archive/mvp.myfeeds.ai/content/images/2025/03/image-50.png)

In the [mvp.MyFeeds.ai](https://mvp.myfeeds.ai/) service, we have a set of APIs for Personas:

[image · `image-53.png`](../../back-office/archive/mvp.myfeeds.ai/content/images/2025/03/image-53.png)

... for [The Hacker News](https://thehackernews.com/?ref=mvp.myfeeds.ai) flows:

[image · `image-52.png`](../../back-office/archive/mvp.myfeeds.ai/content/images/2025/03/image-52.png)

... for the Hacker News articles:

[image · `image-54.png`](../../back-office/archive/mvp.myfeeds.ai/content/images/2025/03/image-54.png)

... for the Hacker News files:

[image · `image-55.png`](../../back-office/archive/mvp.myfeeds.ai/content/images/2025/03/image-55.png)

... and for the [Open Security Summit](https://open-security-summit.org/?ref=mvp.myfeeds.ai) data (although that is not relevant in this article :) )

[image · `image-56.png`](../../back-office/archive/mvp.myfeeds.ai/content/images/2025/03/image-56.png)

#### Looking at the current articles

Looking at the ***hacker-news-articles/current-articles*** article data, we can see that every article in there is currently on Step_9 (the current last step)

[image · `image-57.png`](../../back-office/archive/mvp.myfeeds.ai/content/images/2025/03/image-57.png)

What we need is a new set of articles to process, so let's see how that is currently done.

#### Flow 1 - Downloading the RSS feed

We start the full workflow by invoking the endpoint ***hacker-news-flows/flow-1-download-rss-feed*** which downloads the RSS feed and converts it into an JSON file

[image · `image-67.png`](../../back-office/archive/mvp.myfeeds.ai/content/images/2025/03/image-67.png)

Here is what the ***feed-data.json*** file looks like

[image · `image-68.png`](../../back-office/archive/mvp.myfeeds.ai/content/images/2025/03/image-68.png)

#### Flow 2 - Creating the timeline

Next we need to create the MGraph Timeline, which is done by invoking the ***hacker-news-flows/flow-2-create-articles-timeline ***endpoint:

[image · `image-61.png`](../../back-office/archive/mvp.myfeeds.ai/content/images/2025/03/image-61.png)

The output confirms that all went as planned and that the following 3 files were created:

- hacker_news_timeline - this is the MGraph-DB of the timelines (i.e date/time values) of the 50 articles processed. This file is called feed-timeline.mgraph.json

- hacker_news_timeline_dot_code - this is the DOT Language code (see diagrams as code) created by the MGraph Dot_Exporter. This file is called feed-timeline.mgraph.dot

- hacker_news_timeline_png - this is the Graphviz visualiastion of the DOT code, created by a Serverless function that is fully configured to convert DOT code into PNGs (i.e. images). This file is called feed-timeline.mgraph.pngAll 3 files were stored twice in the cloud storage (in this case S3):

- in the /latest/* folder (overwriting the previous version)

- in the 2025/03/26/11/* folder (ensuring we have a copy of this action). This is an hour specific folder, which in this case is /2025/03/26/11/* (representing the 11th hour of the day 26 of March in 2025, i.e. the time I'm writing this article)Here is what the MGraph of the timeline looks like:

[image · `image-65.png`](../../back-office/archive/mvp.myfeeds.ai/content/images/2025/03/image-65.png)

Here is the DOT language

[image · `image-66.png`](../../back-office/archive/mvp.myfeeds.ai/content/images/2025/03/image-66.png)

And much more interesting and useful, here is what the PNG of the timeline looks like:

[image · `image-59.png`](../../back-office/archive/mvp.myfeeds.ai/content/images/2025/03/image-59.png)

The MGraph above is quite an important one, since it shows the power of the MGraph-DB in creating a graph made of 50x timestamps (i.e. date/time values).

Note how easy it is to find what happened at a particular year, month, day or hour (the nodes at the bottom represent an article)

For more details about this MGraph timeline technology, and how it evolved during multiple coding iterations, see:

- Storing Timestamps in Graph Databases: A Scalable and Semantic Approach (PDF of research paper)

- How Should a Timestamp Be Represented in a Graph?

- More visualisation capabilities to the MGraph-DB "Export to Dot" feature

- First visualization of timestamps from latest 50 articles

- Two visualisations of three Timestamps

- initial visualisation of latest 15 articles

- Visualization of latest 50x articles using multiple GraphViz engines and layouts.

- MGraph-DB timeline is now automatically created and published to S3Also very important in that invocation response data is the ***durations*** section which provides timing details on the duration of each task executed in this flow (this is very important for debugging and keeping an eye on the performance)

The Flows/Tasks technology that is used to create and execute all these "flows", is part of my [OSBot-Utils](https://github.com/owasp-sbot?ref=mvp.myfeeds.ai) open source package. This was inspired by and compatible with the super powerful [Prefect](https://www.prefect.io/?ref=mvp.myfeeds.ai) open source and SaaS technology.

For more details about this Flows/Tasks see:

- OSBot-Utils Flow System Documentation (PDF with the technical details)

- Example of using Flows and Tasks in the IDE

- Source code in GitHub

#### Flow 3 - Extract new Articles

Now that we have an updated timeline, the next step is to call the ***hacker-news-flows/flow-3-flow-extract-new-articles*** endpoint with the date to use as current_path (i.e. the new baseline time for creating the MGraph Diff)

[image · `image-75.png`](../../back-office/archive/mvp.myfeeds.ai/content/images/2025/03/image-75.png)

Here is the invocation response:

[image · `image-64.png`](../../back-office/archive/mvp.myfeeds.ai/content/images/2025/03/image-64.png)

The first file that we can see in the response (created in two locations as before) is the ***feed-timeline-diff.json**, *which is a really good example of the power of graphs to answer a simple but important question: *"Since the last analysis, which articles were added and removed from the RSS Feed?*"

To see how this was done, look at the values of the ***path_previous ***and ***path_current*** also present in the response data.

In this case we have:

- 2025/03/19/21 - which is the 21st hour of the 19th of March 2025

- 2025/03/26/11 - which is the 11th hour of the 26th of March 2025This is where the practice to keep two copies of the files created really helps.

The file in the ***/latest/** *folder has long been overwritten by more recent executions*, *but since we still have the files in the* **2025/03/19/21/* ***folder, we can take a look at the file*** 2025/03/19/21/feed-timeline.mgraph.png ***to see what the timeline MGraph looked like at that time:

[image · `image-69.png`](../../back-office/archive/mvp.myfeeds.ai/content/images/2025/03/image-69.png)

For reference, here is the current timeline file ***2025/03/26/11/feed-timeline.mgraph.png ***looks like

[image · `image-70.png`](../../back-office/archive/mvp.myfeeds.ai/content/images/2025/03/image-70.png)

What we need is a diff of these two graphs.

The MGraph files of these visualisations was used to create the ***feed-timeline-diff.json*** file, which looks like this:

[image · `image-71.png`](../../back-office/archive/mvp.myfeeds.ai/content/images/2025/03/image-71.png)

... and

[image · `image-72.png`](../../back-office/archive/mvp.myfeeds.ai/content/images/2025/03/image-72.png)

This is a MGraph Timeline-Diff object, which contains two main sections: **added_values** and **removed_values**, which in practice are the nodes added and removed between those two graphs.

This data is then used to update the **latest/articles-current.json** files which now contains the entries for the articles ids listed in the **added_values **in the **Step_1__Save__Article **step (and empty data in those ***path_**** variables

[image · `image-73.png`](../../back-office/archive/mvp.myfeeds.ai/content/images/2025/03/image-73.png)

---

Continues [on part 2](https://mvp.myfeeds.ai/how-im-building-personalised-news-feeds-with-semantic-graphs-part-2/)

↑ recovered article ends this site's words resume

[← All recovered posts](index.md) [Back office →](../index.md)

---

*[Site index for agents](../../llms.txt) · [HTML version](https://myfeeds.sgit.ai/back-office/archive/publishing-a-new-personalised-set-of-posts-part-1.html)*
