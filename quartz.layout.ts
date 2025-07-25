import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

// components shared across all pages
export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  afterBody: [],
  footer: Component.Footer({
    links: {
      GitHub: "https://github.com/jackyzha0/quartz",
      "Discord Community": "https://discord.gg/cRFFHYye7t",
    },
  }),
}

// components for pages that display a single page (e.g. a single note)
export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.Breadcrumbs(),
    Component.ArticleTitle(),
    Component.ContentMeta(),
    Component.TagList(),
  ],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Search(),
    Component.Darkmode(),
    Component.Explorer(),
  ],
  right: [
    Component.Graph(
      {
        localGraph: {
          drag: true, // whether to allow panning the view around
          zoom: true, // whether to allow zooming in and out
          depth: 2, // how many hops of notes to display
          scale: 1.5, // default view scale
          repelForce: 1.0, // how much nodes should repel each other
          centerForce: 0.3, // how much force to use when trying to center the nodes
          linkDistance: 50, // how long should the links be by default?
          fontSize: 2.0, // what size should the node labels be?
          opacityScale: 1, // how quickly do we fade out the labels when zooming out?
          removeTags: [], // what tags to remove from the graph
          showTags: true, // whether to show tags in the graph
          enableRadial: false, // whether to constrain the graph, similar to Obsidian
        },
        globalGraph: {
          drag: true,
          zoom: true,
          depth: -1,
          scale: 1,
          repelForce: 20,
          centerForce: 0.3,
          linkDistance: 300,
          fontSize: 1.5, // what size should the node labels be?
          opacityScale: 1, // how quickly do we fade out the labels when zooming out?
          removeTags: [], // what tags to remove from the graph
          showTags: false, // whether to show tags in the graph
          enableRadial: true, // whether to constrain the graph, similar to Obsidian
        },
      }
    ),
    Component.DesktopOnly(Component.TableOfContents()),
    Component.Backlinks(),
  ],
}

// components for pages that display lists of pages  (e.g. tags or folders)
export const defaultListPageLayout: PageLayout = {
  beforeBody: [Component.Breadcrumbs(), Component.ArticleTitle(), Component.ContentMeta()],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Search(),
    Component.Darkmode(),
    Component.Explorer(),
  ],
  right: [],
}
