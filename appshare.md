
Short version (2–3 sentences):

▎ Appshare is a web publishing platform: users drop documents and media into our Mac and Windows apps and get them published as clean, responsive HTML pages. We use our backend infrastructure to convert and restructure documents into semantic HTML, generate layouts, and write summaries, titles and alt text, turning a raw file into a polished, accessible web page in one step.

Longer version (if the form allows more):

▎ Appshare is a web publishing company. Our Mac and Windows desktop apps let anyone send a document (Word, PDF, Markdown, slides) or media (images, audio, video) and get it published as a hosted HTML page, with no web skills required.

▎ We use our backend infrastructure to understand document structure and turn it into clean, semantic, responsive HTML; generate page layouts and styling; write SEO metadata, summaries and image alt text for accessibility; and let users edit published pages in plain language.

▎ We're [stage: e.g. building our MVP / in private beta with N users] and expect API usage to grow with every page published.

▎ We're building Appshare into two layers:
   - Product: converting uploaded documents into clean, semantic, responsive HTML, and generating page metadata,
     summaries and alt text.
 
   - Infrastructure: Appshare runs on our own Kubernetes cluster, managed as code with Ansible (kubeadm, CRI-O,
     Helm, monitoring, firewall). We're using Claude as an operations agent for it: deploying releases, diagnosing incidents
     from monitoring data, and keeping configuration consistent. That lets say a very small team who run a production infrastructure.

   - Security: AI reviews our code and infrastructure continuously. It audits for exposed secrets, hardens authentication and authorization
     across our backend and desktop clients, reviews changes before they ship, and checks cluster and firewall configuration.
     It has already helped us find and fix authorization gaps and tighten session handling.

Desktop Applications

Appshare: publish your documents and media to the web in a few clicks, from your Mac or Windows PC.

▎ Appshare turns your files into web pages. The Mac and Windows apps are your workspace: upload your documents and media, organize and preview them, then publish them in one click. appshare.site is where your audience finds them: every published page can be viewed in any browser and shared by link or email.
▎
▎ Upload whole folders. Choose a folder on your computer, and Appshare uploads its documents and media to your Appshare account. Large files are sent in chunks with a progress bar, so you can see the upload advance.
▎
▎ See everything in one place. Your folders and files are listed in the app, with their type, size and status. Search to find a file quickly.
▎
▎ Preview before you publish. Open PDFs, images, text documents, videos and audio directly in the app. Videos and music stream instantly, without downloading the whole file.
▎
▎ Publish a folder in one click. Each published folder becomes its own page on appshare.site, showing all its files. Unpublish it any time to take it offline, archive what you no longer need, or delete it for good.
▎
▎ Your account, secured. Create an account, sign in, and reset your password from the app. Your login is stored safely by your operating system.
▎
▎ In your language. Appshare speaks English, French, Spanish and German, on Mac and Windows alike. More languages are on the way.
▎
▎ Share with anyone. Every published page has its own address on appshare.site. Copy the link, or send the page by email straight from the web page. Recipients open it in their browser, with no app or account needed.

Appshare for Mac: a native macOS app built with SwiftUI. It feels at home on your Mac: system file picker, built-in video and audio player, and your login kept in the macOS Keychain.

Appshare for Windows: a native Windows app built with .NET MAUI. Pick a folder, watch the upload progress, and browse your files in a clear list. PDFs, images, video and audio open in the app's built-in viewers.
