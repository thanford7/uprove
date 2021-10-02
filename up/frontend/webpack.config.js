const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const { VueLoaderPlugin } = require('vue-loader');
const { WebpackManifestPlugin } = require("webpack-manifest-plugin");
const webpack = require('webpack');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const StylelintPlugin = require('stylelint-webpack-plugin');

const currentTask = process.env.npm_lifecycle_event;
const path = require("path");
const localPath = 'http://localhost:3000/';
const prodPath = '/bundled-assets/';

const postCSSPlugins = [require("postcss-import"), require("postcss-mixins"), require("postcss-simple-vars"), require("postcss-nested"), require("postcss-hexrgba"), require("postcss-color-function"), require("autoprefixer")]

const sassConfig = {
  test: /\.s?[ac]ss$/i,
  use: [
    // Translates CSS into CommonJS
    'css-loader?url=false',
    { loader: "postcss-loader", options: { postcssOptions: {plugins: postCSSPlugins} } },
    // Compiles Sass to CSS
    "sass-loader",
  ],
}

let config = {
  entry: {
    app: './js/main.js'
  },
  plugins: [
    // new BundleAnalyzerPlugin(),
    new VueLoaderPlugin(),
    new StylelintPlugin(),
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery',
      dayjs: 'dayjs',
      'window.jQuery': 'jquery/dist/jquery.min.js',
      Popper: ['popper.js', 'default'],
      Vue: 'vue/dist/vue.runtime.esm.js',
      Vuex: 'vuex/dist/vuex.esm.js',
      _: 'lodash'
    })
  ],
  module: {
    rules: [
      sassConfig,
      {
        test: /\.js$/,
        exclude: /(node_modules)/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        }
      },
      {
        test: /\.vue$/,
        loader: 'vue-loader'
      },
      {
        test: /\.(png|jpe?g|gif)$/i,
        type: 'asset/resource'
      },
      {
        test: /\.(woff|woff2|ttf|eot|ico)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
        type: 'asset/resource'
      },
      {
        test: /\.ts$/,
        exclude: /(node_modules)/,
        use: [{
          loader: 'ts-loader',
        }]
      },
      {
        test: /\.svg$/,
        type: 'asset/resource'
      }
    ],
  },
  resolve: {
    alias: {
      vue: 'vue/dist/vue.runtime.esm.js',  // https://vuejs.org/v2/guide/installation.html#Explanation-of-Different-Builds
    },
    extensions: ['*', '.js', '.vue', '.json', '.scss', '.ts', '.svg']
  }
}

if (currentTask == "devFast") {
  config.devtool = "source-map"
  sassConfig.use.unshift("style-loader")
  config.output = {
    filename: "[name].bundled.js",
    publicPath: localPath
  }
  config.devServer = {
    before: function (app, server) {
       server._watch(["./**/*.js"])
    },
    public: localPath,
    publicPath: localPath,
    disableHostCheck: true,
    contentBase: path.join(__dirname),
    contentBasePublicPath: localPath,
    historyApiFallback: true,
    hot: true,
    port: 3000,
    headers: {
      "Access-Control-Allow-Origin": "*"
    }
  }
  config.mode = "development"
}

if (currentTask == "build" || currentTask == "buildWatch") {
  sassConfig.use.unshift(MiniCssExtractPlugin.loader)
  postCSSPlugins.push(require("cssnano"))
  config.output = {
    publicPath: "up/frontend/bundled-assets/",
    filename: "[name].[chunkhash].js",
    chunkFilename: "[name].[chunkhash].js",
    path: path.resolve(__dirname, "bundled-assets")
  }
  config.mode = "production"
  // config.optimization = {
  //   splitChunks: { chunks: "all" }
  // }
  config.plugins.push(
    new CleanWebpackPlugin({
      cleanAfterEveryBuildPatterns: ['*.LICENSE.txt'],
    }),
    new MiniCssExtractPlugin({ filename: "[name].[chunkhash].css" }),
    new WebpackManifestPlugin({ publicPath: "" }),
    new RunAfterCompile()
  )
}

module.exports = config
