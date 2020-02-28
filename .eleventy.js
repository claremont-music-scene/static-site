module.exports = function (eleventyConfig) {
    // Output directory: _site
    eleventyConfig.addPassthroughCopy("admin/config.yml");
    eleventyConfig.addPassthroughCopy("assets/css");
    eleventyConfig.addPassthroughCopy("assets/js");
    eleventyConfig.addPassthroughCopy("assets/webfonts");
    eleventyConfig.addPassthroughCopy("images");

};