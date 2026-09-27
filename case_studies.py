"""Source-backed product case studies for the Streamlit app.

These cases use company posts and regulatory filings. Product lessons are
interpretations of the cited evidence, not proven single causes of success.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st


CASE_STUDIES = {
    "Worked well": [
        {
            "name": "Duolingo",
            "pattern": "Make the daily habit easy to restart",
            "outcome": (
                "An A/B test reported a 3.3% relative increase in day-14 retention "
                "and a 1% relative increase in daily active learners."
            ),
            "research": (
                "Duolingo separated its streak from a harder daily goal. One lesson was "
                "enough to continue a streak. More learners kept a daily habit, although "
                "fewer completed the full daily goal."
            ),
            "analysis": (
                "Lowering the effort needed for the next useful action helped people return. "
                "The experiment supports this specific change; it does not explain all of "
                "Duolingo's growth."
            ),
            "lesson": "Make the first repeat action small, then test retention and real progress.",
            "sources": [
                ("Duolingo's streak experiment", "https://blog.duolingo.com/improving-the-streak/"),
            ],
        },
        {
            "name": "Spotify",
            "pattern": "Give users a new reason to return",
            "outcome": (
                "Spotify reports that personalized recommendations support large-scale "
                "music discovery, including recurring Discover Weekly and Release Radar playlists."
            ),
            "research": (
                "Spotify asks new users for favorite artists, then combines listening, "
                "search, and other signals to tailor recommendations. Its playlists refresh "
                "regularly rather than leaving users with a static music library."
            ),
            "analysis": (
                "The product reduces the work of finding the next worthwhile song. "
                "Fresh, relevant results can make a return visit useful; Spotify's account "
                "describes the mechanism, but does not isolate its effect on total growth."
            ),
            "lesson": "Use what people do to improve the value of their next visit.",
            "sources": [
                (
                    "Spotify on personalization",
                    "https://newsroom.spotify.com/2021-10-13/adding-that-extra-you-to-your-discovery-oskar-stal-spotify-vice-president-of-personalization-explains-how-it-works/",
                ),
                (
                    "Spotify on music discovery",
                    "https://newsroom.spotify.com/2023-07-20/nearly-2-billion-music-discoveries-happen-on-spotify-every-day-heres-what-listeners-are-finding/",
                ),
            ],
        },
        {
            "name": "WhatsApp",
            "pattern": "Make the core job dependable and trustworthy",
            "outcome": "Meta reported more than 2 billion WhatsApp users in 2020.",
            "research": (
                "WhatsApp describes its goal as simple, reliable, private communication. "
                "It uses end-to-end encryption by default for private messages."
            ),
            "analysis": (
                "Messaging is more useful when the people someone wants to reach are "
                "already there. Reliability and privacy may reduce the cost of choosing it "
                "for important conversations. This is an interpretation, not an experiment "
                "that separates these effects."
            ),
            "lesson": "For a network app, protect the core action and earn trust before adding extras.",
            "sources": [
                (
                    "Meta on WhatsApp's scale and design goal",
                    "https://about.fb.com/news/2020/02/two-billion-users/",
                ),
            ],
        },
        {
            "name": "Canva",
            "pattern": "Lower the skill barrier, then enable collaboration",
            "outcome": "Canva reported more than 170 million monthly users at the end of 2023.",
            "research": (
                "Canva offers editable templates and a drag-and-drop editor. It also "
                "added real-time co-editing and comments, so a design can move through a "
                "team without leaving the product."
            ),
            "analysis": (
                "Templates help a novice get a useful result quickly; collaboration gives "
                "that result a path into a shared workflow. The cited sources document the "
                "features and scale, but do not measure each feature's separate contribution."
            ),
            "lesson": "Help new users finish one good task, then make the result easy to share.",
            "sources": [
                ("Canva's growth report", "https://www.canva.com/newsroom/news/canva-us-growth/"),
                (
                    "Canva on real-time collaboration",
                    "https://www.canva.com/newsroom/news/canva-cements-position-collaboration-platform-amidst-rapid-mau-growth/",
                ),
                ("Canva's editor and templates", "https://www.canva.com/free/"),
            ],
        },
        {
            "name": "Airbnb",
            "pattern": "Build trust into the transaction",
            "outcome": (
                "Airbnb reported 12% year-over-year revenue growth and 16% growth "
                "in gross booking value in Q4 2025."
            ),
            "research": (
                "The service uses identity checks, reviews, secure messaging, and guest "
                "and host protections to help strangers decide whether to book or host."
            ),
            "analysis": (
                "A two-sided marketplace needs both sides to feel safe enough to complete "
                "a transaction. These trust tools address that obstacle, but the sources "
                "do not prove how much growth each tool caused."
            ),
            "lesson": "Make uncertainty and risk visible, then reduce them in the core flow.",
            "sources": [
                ("Airbnb Q4 2025 results", "https://news.airbnb.com/airbnb-q4-2025-financial-results"),
                ("Airbnb's trust features", "https://www.airbnb.com/help/article/4"),
                ("Airbnb identity verification", "https://www.airbnb.com/help/article/3033"),
            ],
        },
    ],
    "Setbacks": [
        {
            "name": "Quibi",
            "pattern": "A polished product still needs a strong use case",
            "outcome": "Quibi announced in October 2020 that it was winding down.",
            "research": (
                "Its founders said the mobile-first premium service did not succeed. "
                "They pointed to a standalone idea that may not have been strong enough, "
                "launch timing during the pandemic, or both."
            ),
            "analysis": (
                "The founders did not identify one proven cause. The case shows why a "
                "large content and technology investment cannot substitute for validating "
                "the viewing occasion and willingness to pay."
            ),
            "lesson": "Test the core use case and payment demand before scaling production.",
            "sources": [
                ("Quibi founders' shutdown letter", "https://quibi-hq.medium.com/an-open-letter-from-quibi-8af6b415377f"),
            ],
        },
        {
            "name": "Google Allo",
            "pattern": "A feature-rich app can lose to an existing default",
            "outcome": "Google ended support for Allo in March 2019 and focused on Messages.",
            "research": (
                "Google moved Allo features such as Smart Reply, GIFs, and desktop "
                "support into Messages. It reported more than 175 million monthly Messages "
                "users and said Messages' momentum drove the decision."
            ),
            "analysis": (
                "Useful features were easier to distribute through a messaging product "
                "people already used. Google did not publish a controlled test showing "
                "that distribution alone caused Allo's closure."
            ),
            "lesson": "Check whether a new standalone app is necessary to deliver the value.",
            "sources": [
                ("Google's Allo and Messages update", "https://blog.google/products-and-platforms/products/messages/latest-messages-allo-duo-and-hangouts/"),
            ],
        },
        {
            "name": "Google+",
            "pattern": "Reach is meaningless without sustained use",
            "outcome": "Google shut down the consumer Google+ product.",
            "research": (
                "Google reported limited adoption and engagement: 90% of consumer "
                "Google+ sessions lasted less than five seconds. It also described the "
                "difficulty of maintaining its APIs and a discovered privacy bug."
            ),
            "analysis": (
                "A familiar brand and substantial engineering effort did not produce "
                "meaningful repeat use. The API and privacy burden made a low-use "
                "product harder to justify maintaining."
            ),
            "lesson": "Measure useful sessions and retention, and include trust costs in the plan.",
            "sources": [
                ("Google's Project Strobe findings", "https://blog.google/innovation-and-ai/technology/safety-security/project-strobe/"),
            ],
        },
        {
            "name": "Google Stadia",
            "pattern": "Technical success is not market traction",
            "outcome": "Google wound down Stadia's consumer service in January 2023.",
            "research": (
                "Google said Stadia's streaming technology was strong but the consumer "
                "service had not gained the expected user traction. It refunded hardware "
                "and content purchases."
            ),
            "analysis": (
                "A technically capable platform is only part of an app's value. Google "
                "did not identify one cause of weak adoption, so the lesson concerns "
                "testing the whole offer rather than assuming good technology is enough."
            ),
            "lesson": "Validate the complete user proposition, not only the technical demo.",
            "sources": [
                ("Google's Stadia wind-down", "https://blog.google/products-and-platforms/products/stadia/message-on-stadia-streaming-strategy/"),
            ],
        },
        {
            "name": "Snapchat's 2018 redesign",
            "pattern": "A major redesign can disrupt a working habit",
            "outcome": (
                "Snap said daily active users declined in 2018 primarily because of "
                "design changes and ongoing Android performance issues."
            ),
            "research": (
                "Snap's annual filing ties the decline to its app redesign and Android "
                "performance. This was a setback for a continuing app, not a shutdown "
                "of Snapchat."
            ),
            "analysis": (
                "Changes to familiar paths can interrupt established behavior, while "
                "uneven platform quality can compound the effect. Snap's filing does "
                "not isolate the exact contribution of each factor."
            ),
            "lesson": "Test big workflow changes with cohorts and watch retention by platform.",
            "sources": [
                ("Snap 2018 annual filing", "https://www.sec.gov/Archives/edgar/data/1564408/000156459019002053/snap-10k_20181231.htm"),
            ],
        },
    ],
}


def render_research_case_studies() -> None:
    """Render ten researched examples with directly linked primary sources."""
    st.title("Why Apps Succeed or Struggle")
    st.markdown(
        "Ten documented product cases show different paths to a strong result or a setback. "
        "The five setbacks include discontinued products and one damaging redesign; "
        "Snapchat itself did not shut down."
    )
    st.info(
        "These case studies use company reports, official product posts, and a public "
        "filing. **Reported facts** and **our interpretation** are separated below. "
        "The app-market CSV does not contain the review text, experiments, or business "
        "outcomes needed to explain these stories by itself."
    )

    for group, cases in CASE_STUDIES.items():
        st.subheader("What worked" if group == "Worked well" else "What went wrong")
        summary = pd.DataFrame(
            [
                {"App": case["name"], "Product pattern": case["pattern"]}
                for case in cases
            ]
        )
        st.dataframe(summary, width="stretch", hide_index=True)
        for number, case in enumerate(cases, start=1):
            with st.expander(f"{number}. {case['name']} — {case['pattern']}", expanded=number == 1):
                st.markdown("**Result**")
                st.write(case["outcome"])
                st.markdown("**What the sources show**")
                st.write(case["research"])
                st.markdown("**Why it matters — interpretation**")
                st.write(case["analysis"])
                st.markdown("**Lesson for an app maker**")
                st.write(case["lesson"])
                links = " · ".join(
                    f"[{title}]({url})" for title, url in case["sources"]
                )
                st.markdown(f"**Sources:** {links}")

    st.subheader("What the ten cases suggest")
    st.markdown(
        "- **Give people a reason to return.** Duolingo made a daily action easier; "
        "Spotify made the next visit useful. Google+ shows how weak session engagement "
        "can undermine a large product.\n"
        "- **Meet people where their task already happens.** WhatsApp benefited from "
        "a dependable communication network, while Google moved Allo's useful features "
        "into the more established Messages app.\n"
        "- **Validate the whole experience.** Canva and Airbnb address creation and "
        "trust barriers. Quibi and Stadia show that high investment or strong technology "
        "does not, by itself, establish demand.\n"
        "- **Protect working habits.** Snap's redesign and Android problems show why "
        "major changes need close monitoring by platform."
    )
    st.caption("These are interpretations across selected cases, not universal rules.")

    with st.expander("How to read these cases"):
        st.markdown(
            "- The cases were chosen for documented product decisions and outcomes, "
            "not for their position in the app-market CSV. Several are absent from that dataset.\n"
            "- Company sources can explain their own decisions and report measurements, "
            "but may omit other causes. A lesson is a reasoned interpretation unless a "
            "controlled experiment directly supports it.\n"
            "- Success and failure refer to the specific outcome described in each case. "
            "One weak release does not mean an entire app or company failed."
        )
