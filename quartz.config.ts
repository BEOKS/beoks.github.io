import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * Quartz 4.0 Configuration
 *
 * See https://quartz.jzhao.xyz/configuration for more information.
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "🪴 Beoks Blog",
    pageTitleSuffix: " | Beoks Blog",
    enableSPA: true,
    enablePopovers: true,
    analytics: {
      provider: "plausible",
    },
    locale: "ko-KR",
    baseUrl: "quartz.jzhao.xyz",
    ignorePatterns: ["private", "templates", ".obsidian"],
    defaultDateType: "created",
    generateSocialImages: false,
    // Use homePageLayout for the index page
    pageLayoutMapping: {
      "index": "homePageLayout",
    },
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Inter",
        body: "Inter",
        code: "JetBrains Mono",
      },
      colors: {
        lightMode: {
          light: "#ffffff",
          lightgray: "#ececec",
          gray: "#c2c2c2",
          darkgray: "#3d3d3d",
          dark: "#111111",
          secondary: "#3056a4",
          tertiary: "#5b7fce",
          highlight: "rgba(48, 86, 164, 0.07)",
          textHighlight: "#fff2a8",
        },
        darkMode: {
          light: "#1a1a1a",
          lightgray: "#2b2b2b",
          gray: "#4a4a4a",
          darkgray: "#c9c9c9",
          dark: "#f2f2f2",
          secondary: "#8ab4f8",
          tertiary: "#a9c7ff",
          highlight: "rgba(138, 180, 248, 0.10)",
          textHighlight: "#63530099",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "git", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: true }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.NotFoundPage(),
    ],
  },
}

export default config
