from cat_app import db
from cat_app.models import Product, Category

db.drop_all()
db.create_all()

design = Category(name='Design')
process = Category(name='Process')
prog = Category(name='Programming')
music = Category(name='Music')

prods = [
    Product(name="Peopleware",
            subhead="Productive Projects and Teams",
            description="""Few books in computing have had as profound an
            influence on software management as Peopleware . The unique insight
            of this longtime best seller is that the major issues of software
            development are human, not technical. They&rsquo;re not easy issues;
            but solve them, and you&rsquo;ll maximize your chances of
            success.""",
            category=prog,
            author="Tom DeMarco",
            year=2013),
    Product(name="The Mythical Man-Month",
            subhead="Essays on Software Engineering, Anniversary Edition",
            description="""Few books on software project management have been as
               influential and timeless as The Mythical Man-Month. With a blend
               of software engineering facts and thought-provoking opinions,
               Fred Brooks offers insight for anyone managing complex projects.
               These essays draw from his experience as project manager for the
               IBM System/360 computer family and then for OS/360, its massive
               software system. Now, 20 years after the initial publication of
               his book, Brooks has revisited his original ideas and added new
               thoughts and advice, both for readers already familiar with his
               work and for readers discovering it for the first time.""",
            category=prog,
            author="Frederick P. Brooks Jr.",
            year=1995),
    Product(name="Clean Code",
            subhead="A Handbook of Agile Software Craftsmanship",
            description="""Even bad code can function. But if code isn&rsquo;t
                clean, it can bring a development organization to its knees.
                Every year, countless hours and significant resources are lost
                because of poorly written code. But it doesn&rsquo;t have to be
                that way.""",
            category=prog,
            author="Robert C. Martin",
            year=2008),
    Product(name="Extreme Programming Explained",
            subhead="Embrace Change",
            description="""Whether you have a small team that is already closely
                aligned with your customers or a large team in a gigantic or
                multinational organization, you will find in these pages a
                wealth of ideas to challenge, inspire, and encourage you and
                your team members to substantially improve your software
                development.""",
            category=prog,
            author="Robert C. Martin",
            year=2008),
    Product(name="Becoming a Better Programmer",
            subhead="A Handbook for People Who Care About Code",
            description="""If you&rsquo;re passionate about programming and want
                to get better at it, you&rsquo;ve come to the right source. Code
                Craft author Pete Goodliffe presents a collection of useful
                techniques and approaches to the art and craft of programming
                that will help boost your career and your well-being.""",
            category=prog,
            author="Pete Goodliffe",
            year=2014),
    Product(name="The Agile Culture",
            subhead="Leading through Trust and Ownership",
            description="""The Agile Culture gives you proven models, pragmatic
                tools, and handy worksheets for doing just that. Building on
                their experience helping hundreds of companies, three
                world-class experts help you align and unleash the talents of
                everyone in your organization. Step by step, you&rsquo;ll learn
                how to move toward a culture of trust, in which everyone knows,
                owns, and improves the results. You&rsquo;ll learn practical
                ways to refocus on differentiators and value, resurrect energy
                and innovation, deal more honestly with ambiguity and risk, and
                overcome resistance, no matter where it comes from. This text
                will help you go beyond buzzwords to transform the way you
                deliver software&mdash;so you can delight customers, colleagues,
                and executives.""",
            category=process,
            author="Pollyanna Pixton",
            year=2014),
    Product(name="Lean UX",
            subhead="Applying Lean Principles to Improve User Experience",
            description="""The Lean UX approach to interaction design is
                tailor-made for today&rsquo;s web-driven reality. In this
                insightful book, leading advocate Jeff Gothelf teaches you
                valuable Lean UX principles, tactics, and techniques from the
                ground up&mdash;how to rapidly experiment with design ideas,
                validate them with real users, and continually adjust your
                design based on what you learn.""",
            category=process,
            author="Jeff Gothelf",
            year=2013),
    Product(name="Don't Make Me Think, Revisited",
            subhead="A Common Sense Approach to Web Usability",
            description="""Since Don&rsquo;t Make Me Think was first published
                in 2000, hundreds of thousands of Web designers and developers
                have relied on usability guru Steve Krug&rsquo;s guide to help
                them understand the principles of intuitive navigation and
                information design. Witty, commonsensical, and eminently
                practical, it&rsquo;s one of the best-loved and most recommended
                books on the subject.""",
            category=design,
            author="Steve Krug",
            year=2013),
    Product(name="Sketching User Experiences",
            subhead="Getting the Design Right and the Right Design",
            description="""Sketching User Experiences approaches design and
                design thinking as something distinct that needs to be better
                understood-by both designers and the people with whom they need to
                work- in order to achieve success with new products and systems.
                So while the focus is on design, the approach is holistic.
                Hence, the book speaks to designers, usability specialists, the
                HCI community, product managers, and business executives. There
                is an emphasis on balancing the back-end concern with usability
                and engineering excellence (getting the design right) with an
                up-front investment in sketching and ideation (getting the right
                design). Overall, the objective is to build the notion of
                informed design: molding emerging technology into a form that
                serves our society and reflects its values.""",
            category=design,
            author="Bill Buxton",
            year=2010),
    Product(name="The User Experience Team of One",
            subhead="A Research and Design Survival Guide",
            description="""The User Experience Team of One prescribes a range of
                approaches that have big impact and take less time and fewer
                resources than the standard lineup of UX deliverables. Whether
                you want to cross over into user experience or you're a seasoned
                practitioner trying to drag your organization forward, this book
                gives you tools and insight for doing more with less.""",
            category=design,
            author="Leah Buley",
            year=2013),
    Product(name="Interviewing Users",
            subhead="How to Uncover Compelling Insights",
            description="""Interviewing is a foundational user research tool
                that people assume they already possess. Everyone can ask
                questions, right? Unfortunately, that's not the case.
                Interviewing Users provides invaluable interviewing techniques
                and tools that enable you to conduct informative interviews with
                anyone. You'll move from simply gathering data to uncovering
                powerful insights about people.""",
            category=design,
            author="Steve Portigal",
            year=2013),
    Product(name="Fifty Quick Ideas To Improve Your User Stories",
            description="""This book will help you write better user stories,
            spot and fix common issues, split stories so that they are smaller
            but still valuable, and deal with difficult stuff like crosscutting
            concerns, long-term effects and non-functional requirements. Above
            all, this book will help you achieve the promise of agile and
            iterative delivery: to ensure that the right stuff gets delivered
            through productive discussions between delivery team members and
            business stakeholders. """,
            category=process,
            author="Gojko Adzic",
            year=2014),
    Product(name="The UX Book",
            subhead="Process and Guidelines for Ensuring a Quality User "
                    "Experience",
            description="""The UX Book: Process and Guidelines for Ensuring a
                Quality User Experience aims to help readers learn how to create
                and refine interaction designs that ensure a quality user
                experience (UX). The book seeks to expand the concept of
                traditional usability to a broader notion of user experience; to
                provide a hands-on, practical guide to best practices and
                established principles in a UX lifecycle; and to describe a
                pragmatic process for managing the overall development
                effort.""",
            category=design,
            author="Rex Hartson, Pardha S. Pyla",
            year=2012),
    Product(name="User-Centered Design",
            subhead="A Developer's Guide to Building User-Friendly "
                    "Applications",
            description="""How do you design engaging applications that people
                love to use? This book demonstrates several ways to include
                valuable input from potential clients and customers throughout
                the process. With practical guidelines and insights from his own
                experience, author Travis Lowdermilk shows you how usability and
                user-centered design will dramatically change the way people
                interact with your application.""",
            category=design,
            author="Travis Lowdermilk",
            year=2013),
    Product(name="Our Band Could Be Your Life",
            subhead="Scenes from the American Indie Underground, 1981-1991",
            description="""This is the never-before-told story of the musical
                revolution that happened right under the nose of the Reagan
                Eighties--when a small but sprawling network of bands, labels,
                fanzines, radio stations, and other subversives reenergized
                American rock with punk rock's do-it-yourself credo and created
                music that was deeply personal, often brilliant, always
                challenging, and immensely influential. This sweeping chronicle
                of music, politics, drugs, fear, loathing, and faith has been
                recognized as an indie rock classic in its own right.""",
            category=music,
            author="Michael Azerrad",
            year=2012),
    Product(name="Lipstick Traces",
            subhead="A Secret History of the 20th Century",
            description="""This is a secret history of modern times, told by way
                of what conventional history tries to exclude. Lipstick Traces
                tells a story as disruptive and compelling as the century
                itself.""",
            category=music,
            author="Greil Marcus",
            year=2009),
    Product(name="Rip It Up and Start Again",
            subhead="Postpunk 1978-1984",
            description="""Rip It Up and Start Again is the first book-length
                exploration of the wildly adventurous music created in the years
                after punk. Renowned music journalist Simon Reynolds celebrates
                the futurist spirit of such bands as Joy Division, Gang of Four,
                Talking Heads, and Devo, which resulted in endless innovations
                in music, lyrics, performance, and style and continued into the
                early eighties with the video-savvy synth-pop of groups such as
                Human League, Depeche Mode, and Soft Cell, whose success
                coincided with the rise of MTV. Full of insight and anecdotes
                and populated by charismatic characters, Rip It Up and Start
                Again re-creates the idealism, urgency, and excitement of one of
                the most important and challenging periods in the history of
                popular music.""",
            category=music,
            author="Simon Reynolds",
            year=2006),
    Product(name="Psychotic Reactions and Carburetor Dung",
            subhead="Rock'N'Roll as Literature and Literature as Rock 'N'Roll",
            description="""Vintage presents the paperback edition of the wild
                and brilliant writings of Lester Bangs--the most outrageous and
                popular rock critic of the 1970s--edited and with an
                introduction by the reigning dean of rack critics, Greil Marcus.
                Advertising in Rolling Stone and other major publications.""",
            category=music,
            author="Lester Bangs",
            year=2013),
    Product(name="Please Kill Me",
            subhead="The Uncensored Oral History of Punk",
            description="""A <i>Time Out</i> and <i>Daily News</i> Top Ten Book
                of the Year upon its initial release, Please Kill Me is the
                first oral history of the most nihilist of all pop movements.
                Iggy Pop, Danny Fields, Dee Dee and Joey Ramone, Malcom McLaren,
                Jim Carroll, and scores of other famous and infamous punk
                figures lend their voices to this definitive account of that
                outrageous, explosive era. From its origins in the twilight
                years of Andy Warhol&rsquo;s New York reign to its last gasps
                as eighties corporate rock, the phenomenon known as punk is
                scrutinized, eulogized, and idealized by the people who were
                there and who made it happen.""",
            category=music,
            author="Gillian McCain, Legs McNeil",
            year=2014),
    Product(name="We Got the Neutron Bomb",
            subhead="The Untold Story of L.A. Punk",
            description="""Taking us back to late &rsquo;70s and early
                &rsquo;80s Hollywood&mdash;pre-crack, pre-AIDS,
                pre-Reagan&mdash;We Got the Neutron Bomb re-creates word for
                word the rage, intensity, and anarchic glory of the Los Angeles
                punk scene, straight from the mouths of the scenesters,
                zinesters, groupies, filmmakers, and musicians who were
                there.""",
            category=music,
            author="Marc Spitz",
            year=2010)
]

db.session.add_all(prods)
db.session.commit()
