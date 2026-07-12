import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

// A minimal top navigation bar shared across pages:
// site title on the left, search + dark-mode toggle on the right.
const navbar = [
  Component.PageTitle(),
  Component.Spacer(),
  Component.Search(),
  Component.Darkmode(),
]

// components shared across all pages
export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: navbar,
  afterBody: [],
  footer: Component.Footer({
    links: {
      GitHub: "https://github.com/BEOKS",
    },
  }),
}

// components for pages that display a single page (e.g. a single note)
export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.ArticleTitle(),
    Component.ContentMeta(),
    Component.TagList(),
  ],
  left: [],
  right: [],
  afterBody: [
    Component.RecentNotes({
      title: "최근 게시글",
      limit: 5,
      showTags: true,
    }),
  ],
}

// components for pages that display lists of pages  (e.g. tags or folders)
export const defaultListPageLayout: PageLayout = {
  beforeBody: [Component.ArticleTitle(), Component.ContentMeta()],
  left: [],
  right: [],
}

// components for the home page
export const homePageLayout: PageLayout = {
  beforeBody: [
    // No article title / date meta on the home page — just the post list.
    Component.RecentNotes({
      title: "전체 게시글",
      limit: Infinity,
      showTags: true,
    }),
  ],
  left: [],
  right: [],
}
