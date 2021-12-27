const {BundleAnalyzerPlugin} = require('webpack-bundle-analyzer');
const {CleanWebpackPlugin} = require('clean-webpack-plugin');
const {VueLoaderPlugin} = require('vue-loader');
const {WebpackManifestPlugin} = require('webpack-manifest-plugin');
const {WebpackPluginServe: Serve} = require('webpack-plugin-serve');
const CompressionPlugin = require("compression-webpack-plugin");
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const webpack = require('webpack');
const zlib = require("zlib");

const path = require('path');
const postCSSPlugins = [require("postcss-import"), require("postcss-mixins"), require("postcss-simple-vars"), require("postcss-nested"), require("postcss-hexrgba"), require("postcss-color-function"), require("autoprefixer")]


module.exports = function (env, argv) {
    if (env.WEBPACK_BUILD) {
        postCSSPlugins.push(require('cssnano'));
    }
    const cfg = {
        mode: (env.prod) ? 'production' : 'development',
        context: __dirname,
        devtool: 'source-map',
        entry: [path.resolve(__dirname, 'up/frontend/js/main.js')],
        output: {
            path: path.resolve(__dirname, 'up/frontend/dist/'),
            publicPath: '/static/',
            filename: `[name].js`,
            chunkFilename: '[name].[chunkhash].js',
        },
        plugins: [
            // new BundleAnalyzerPlugin(),
            new MiniCssExtractPlugin({
                filename: '[name].css',
                chunkFilename: '[name].[hash].css'
            }),
            new webpack.DefinePlugin({
                PRODUCTION: Boolean(env.production),
                __VUE_OPTIONS_API__: true,
                __VUE_PROD_DEVTOOLS__: false
            }),
            new VueLoaderPlugin(),
            new CleanWebpackPlugin(),
            new CompressionPlugin({
                filename: "[path][base].br",
                algorithm: "brotliCompress",
                test: /\.(js|css|html|svg)$/,
                compressionOptions: {
                    params: {
                        [zlib.constants.BROTLI_PARAM_QUALITY]: 11,
                    },
                },
                threshold: 10240,
                minRatio: 0.8,
                deleteOriginalAssets: false,
            }),
            new webpack.ProvidePlugin({
                $: 'jquery',
                jQuery: 'jquery',
            }),
            new WebpackManifestPlugin({
                publicPath: '',
                writeToFileEmit: true
            })
        ],
        resolve: {
            alias: {
                vue: '@vue/runtime-dom',  // https://v3.vuejs.org/guide/installation.html#release-notes
            },
            extensions: ['.tsx', '.ts', '.js', '.vue', '.scss']
        },
        module: {
            rules: [
                {
                    test: /\.s?[ac]ss$/i,
                    use: [
                        MiniCssExtractPlugin.loader,
                        // Translates CSS into CommonJS
                        'css-loader?url=false',
                        {loader: 'postcss-loader', options: {postcssOptions: {plugins: postCSSPlugins}}},
                        // Compiles Sass to CSS
                        'sass-loader',
                    ],
                },
                {
                    test: /\.js$/,
                    include: path.resolve(__dirname, 'up/frontend/js'),
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
                chunks: 'all',
                maxSize: 600000,
                cacheGroups: {
                    commons: {
                        test: /[\\/]node_modules[\\/]/,
                        name: 'external-packages',
                        chunks: 'all'
                    }
                }
            }
        },
    }

    if (env.prod) {
        cfg.module.rules.push({
            test: /\.(js|vue)$/,
            enforce: 'pre',
            include: path.resolve(__dirname, 'up/frontend/js'),
            exclude: /node_modules/,
            use: [{
                loader: 'webpack-strip-block',
                options: {
                    start: 'dev-only',
                    end: 'end-dev-only'
                }
            }]
        });
    } else {
        // Add dev server
        cfg.entry.unshift('webpack-plugin-serve/client');
        cfg.plugins.push(new Serve({
            host: '0.0.0.0',
            port: 3000,
            historyFallback: {
                index: '/404/'
            },
            log: {level: 'debug'},
            static: path.join(__dirname, 'up/frontend/dist'),
            middleware: (app, builtins) => {
                app.use(builtins.proxy('!/static', {target: 'http://localhost:8000'}));
            }
        }));
        cfg.watch = true;
    }

    return cfg;
}
