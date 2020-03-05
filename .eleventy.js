const markdownShortcode = require("eleventy-plugin-markdown-shortcode");

module.exports = function (eleventyConfig) {
    // Output directory: _site
    eleventyConfig.addPassthroughCopy("admin");
    eleventyConfig.addPassthroughCopy("assets/css");
    eleventyConfig.addPassthroughCopy("assets/js");
    eleventyConfig.addPassthroughCopy("assets/webfonts");
    eleventyConfig.addPassthroughCopy("images");

    eleventyConfig.addPlugin(markdownShortcode);

};
