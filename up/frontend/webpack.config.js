const {BundleAnalyzerPlugin} = require('webpack-bundle-analyzer');
const {CleanWebpackPlugin} = require('clean-webpack-plugin');
const {VueLoaderPlugin} = require('vue-loader');
const webpack = require('webpack');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

const path = require('path');
const postCSSPlugins = [require("postcss-import"), require("postcss-mixins"), require("postcss-simple-vars"), require("postcss-nested"), require("postcss-hexrgba"), require("postcss-color-function"), require("autoprefixer")]


module.exports = function (env, argv) {
    const task = env.npm_lifecycle_event;
    const isFullBuild = ['build', 'buildWatch'].includes(task);
    if (isFullBuild) {
        postCSSPlugins.push(require('cssnano'));
    }
    const cfg = {
        mode: (env.production) ? 'production' : 'development',
        context: __dirname,
        devtool: (env.prod) ? 'source-map' : 'eval',  // https://webpack.js.org/configuration/devtool/
        entry: [
            require.resolve('webpack-dev-server/client'),
            path.resolve(__dirname, './js/main.js')
        ].filter(Boolean),
        output: {
            path: path.resolve(__dirname, './dist'),
            publicPath: '/dist/',
            filename: `[name]${(env.production) ? '.[chunkhash]' : ''}.js`,
            chunkFilename: '[name].[chunkhash].js',
        },
        plugins: [
            // new BundleAnalyzerPlugin(),
            new VueLoaderPlugin(),
            new CleanWebpackPlugin({
                    cleanAfterEveryBuildPatterns: ['*.LICENSE.txt'],
            })
        ],
        resolve: {
            alias: {
                vue: '@vue/runtime-dom',  // https://v3.vuejs.org/guide/installation.html#release-notes
            },
            extensions: ['.tsx', '.ts', '.js', '.vue']
        },
        module: {
            rules: [
                {
                    test: /\.s?[ac]ss$/i,
                    use: [
                        ...(isFullBuild) ? [MiniCssExtractPlugin.loader] : [],
                        'style-loader',
                        // Translates CSS into CommonJS
                        'css-loader?url=false',
                        {loader: 'postcss-loader', options: {postcssOptions: {plugins: postCSSPlugins}}},
                        // Compiles Sass to CSS
                        'sass-loader',
                    ],
                },
                {
                    test: /\.js$/,
                    include: path.resolve(__dirname, 'js'),
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
                    loader: 'vue-loader',
                    exclude: /node_modules/,
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
        optimization: {
            splitChunks: {
                cacheGroups: {
                    commons: {
                        test: /[\\/]node_modules[\\/]/,
                        name: 'external-packages',
                        chunks: 'all'
                    }
                }
            }
        },
        devServer: {
            watchFiles: ['./js/*.js', './js/*.vue', './js/**/*.js', './js/**/*.vue'],
            historyApiFallback: true,
            hot: true,
            port: 3000,
            headers: {
                'Access-Control-Allow-Origin': '*'
            },
        }
    }

    if (env.production) {
        cfg.module.rules.push({
            test: /\.(js|vue)$/,
            enforce: 'pre',
            include: path.resolve(__dirname, 'js'),
            exclude: /node_modules/,
            use: [{
                loader: 'webpack-strip-block',
                options: {
                    start: 'dev-only',
                    end: 'end-dev-only'
                }
            }]
        });
    }

    return cfg;
}
