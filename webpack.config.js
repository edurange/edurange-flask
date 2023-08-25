const path = require('path');
const webpack = require('webpack');
/*
 * Webpack Plugins
 */
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const ProductionPlugins = [
  // production webpack plugins go here
  new webpack.DefinePlugin({
    "process.env": {
      NODE_ENV: JSON.stringify("production")
    }
  })
]

const debug = (process.env.NODE_ENV !== 'production');
const rootAssetPath = path.join(__dirname, 'assets');

// MIGRATION NOTE:  Because the new React UI only has a single entry point (EduRangeEntry.js),
//                  there is no longer any need for any of the other entry 'items' we 
//                  were using for react recently (like for Notifications or etc.).
//                  They have been temporarily disabled/retained. Soon they may be deleted.
//                  
//                  It is POSSIBLE some of these items are still in use by the legacy app,
//                  however (tests show they are not, but better safe than sorry),
//                  so for the time being, they will just be disabled/commented.

module.exports = [
  {
    // configuration
    context: __dirname,
    entry: {
      main_js: './assets/js/main',
      main_css: [
        path.join(__dirname, 'node_modules', 'bootstrap', 'dist', 'css', 'bootstrap.css'), // required by legacy 
        path.join(__dirname, 'assets', 'fontawesome', 'css', 'all.css'), // required by legacy
        path.join(__dirname, 'assets', 'css', 'style.css'), // required by legacy
        // path.join(__dirname, 'react','assets', 'css','unified', 'pucs.css'), // probably unneeded, leave for now
      ],
    },
    mode: debug,
    output: {
      chunkFilename: "[id].js",
      filename: "[name].bundle.js",
      path: path.join(__dirname, "edurange_refactored", "static", "build"),
      publicPath: "/static/build/",
      library: "lib",
      libraryTarget: "var"
    },
    resolve: {
      extensions: [".js", ".jsx", ".css"]
    },
    devtool: debug ? "eval-source-map" : false,
    plugins: [
      new MiniCssExtractPlugin({ filename: "[name].bundle.css" }),
      new webpack.ProvidePlugin({ $: "jquery", jQuery: "jquery" })
    ].concat(debug ? [] : ProductionPlugins),
    module: {
      rules: [
        {
          test: /\.less$/,
          use: [
            {
              loader: MiniCssExtractPlugin.loader,
              options: {
                hmr: debug,
              },
            },
            'css-loader!less-loader',
          ],
        },
        {
          test: /\.css$/,
          use: [
            {
              loader: MiniCssExtractPlugin.loader,
              options: {
                hmr: debug,
              },
            },
            'css-loader',
          ],
        },
        { test: /\.html$/, loader: 'raw-loader' },
        { test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: 'url-loader', options: { limit: 10000, mimetype: 'application/font-woff' } },
        {
          test: /\.(ttf|eot|svg|png|jpe?g|gif|ico)(\?.*)?$/i,
          loader: `file-loader?context=${rootAssetPath}&name=[path][name].[ext]`
        },
        { test: /\.js$/, exclude: /node_modules/, loader: 'babel-loader', query: { presets: ["@babel/preset-env"], cacheDirectory: true } },
      ],
    }
  },

// required by React / new UI (confirmed)
  {
    context: path.join(__dirname, '/edurange_refactored/react/entry/'),
    entry: {
      EduRangeEntry: './EduRangeEntry'
    },
    output: {
      chunkFilename: "[id].js",
      filename: "[name].bundle.js",
      path: path.join(__dirname, "edurange_refactored", "static", "build"),
      publicPath: "/static/build/",
      library: "lib",
      libraryTarget: "var"
    },
    resolve: {
      extensions: [".js", ".jsx", ".css"]
    },
    plugins: [
      new MiniCssExtractPlugin({ filename: "[name].bundle.css" }),
    ],
    module: {
      rules: [
        {
          test: /\.?js(x)?$/,
          use: {
            loader: "babel-loader",
            options: {
              presets: ['@babel/preset-env', '@babel/preset-react']
            }
          },
        },
        {
          test: /\.css$/,
          use: [
            {
              loader: MiniCssExtractPlugin.loader,
              options: {
                hmr: debug,
              },
            },
            'css-loader',
          ],
        },
        {
          test: /\.(ttf|eot|svg|png|jpe?g|gif|ico)(\?.*)?$/i,
          loader: `file-loader?name=[path][name].[ext]`
        }
      ]
    }
  },


// required by earlier jinja/react UI
  {

    context: path.join(__dirname, '/edurange_refactored/templates/student_view/components/'),
    entry: {
      student_scenario: './scenario/scenario.component',
    },
    output: {
      chunkFilename: "[id].js",
      filename: "[name].bundle.js",
      path: path.join(__dirname, "edurange_refactored", "static", "build"),
      publicPath: "/static/build/",
      library: "lib",
      libraryTarget: "var"

    },
    resolve: {
      extensions: [".js", ".jsx", ".css"]
    },
    plugins: [
      new MiniCssExtractPlugin({ filename: "[name].bundle.css" }),
    ],
    module: {
      rules: [
        {
          test: /\.?js(x)?$/,
          use: {
            loader: "babel-loader",
            options: {
              presets: ['@babel/preset-env', '@babel/preset-react']
            }
          },
        },
        {
          test: /\.css$/,
          use: [
            {
              loader: MiniCssExtractPlugin.loader,
              options: {
                hmr: debug,
              },
            },
            'css-loader',
          ],
        }
      ]
    }
  },

// required by earlier jinja/react UI
{
    context: path.join(__dirname, '/edurange_refactored/templates/instructor_view/components/'),
    entry: {
      instructor_view: './instructor_view/instructor_view.component',
    },
    output: {
      chunkFilename: "[id].js",
      filename: "[name].bundle.js",
      path: path.join(__dirname, "edurange_refactored", "static", "build"),
      publicPath: "/static/build/",
      library: "lib",
      libraryTarget: "var"

    },
    resolve: {
      extensions: [".js", ".jsx", ".css"]
    },
    plugins: [
      new MiniCssExtractPlugin({ filename: "[name].bundle.css" }),
    ],
    module: {
      rules: [
        {
          test: /\.?js(x)?$/,
          use: {
            loader: "babel-loader",
            options: {
              presets: ['@babel/preset-env', '@babel/preset-react']
            }
          },
        },
        {
          test: /\.css$/,
          use: [
            {
              loader: MiniCssExtractPlugin.loader,
              options: {
                hmr: debug,
              },
            },
            'css-loader',
          ],
        }
      ]
    }
  },
// required by earlier jinja/react UI
{
    context: path.join(__dirname, '/edurange_refactored/templates/accountmgmt/components/'),
    entry: {
      accountmgmt: './accountmgmt',
    },
    output: {
      chunkFilename: "[id].js",
      filename: "[name].bundle.js",
      path: path.join(__dirname, "edurange_refactored", "static", "build"),
      publicPath: "/static/build/",
      library: "lib",
      libraryTarget: "var"
    },
    resolve: {
      extensions: [".js", ".jsx", ".css"]
    },
    plugins: [
      new MiniCssExtractPlugin({ filename: "[name].bundle.css" }),
    ],
    module: {
      rules: [
        {
          test: /\.?js(x)?$/,
          use: {
            loader: "babel-loader",
            options: {
              presets: ['@babel/preset-env', '@babel/preset-react']
            }
          },
        },
        {
          test: /\.css$/,
          use: [
            {
              loader: MiniCssExtractPlugin.loader,
              options: {
                hmr: debug,
              },
            },
            'css-loader',
          ],
        }
      ]
    }
  },
];


  // -  The notifications entry was disabled to stop an error but it may 
  //    be required by the legacy app.
  // -  After some testing, commenting this seems to not cause problems, 
  //    but i'll leave it here for now.

  // -  The 'home_router' entry was disabled because it appears to be
  //    unused for the new UI (and was never used by the legacy app)
  // -  The 'home_router' entry should remain here, commented out, until it 
  //    is 100% confirmed to be unneeded.

  // {
  //   context: path.join(__dirname, 'edurange_refactored/react/pages/home/src/'),
  //   entry: {
  //     Home_router: './Home_router'
  //   },
  //   output: {
  //     chunkFilename: "[id].js",
  //     filename: "[name].bundle.js",
  //     path: path.join(__dirname, "edurange_refactored", "static", "build"),
  //     publicPath: "/static/build/",
  //     library: "lib",
  //     libraryTarget: "var"
  //   },
  //   resolve: {
  //     extensions: [".js", ".jsx", ".css"]
  //   },
  //   plugins: [
  //     new MiniCssExtractPlugin({ filename: "[name].bundle.css" }),
  //   ],
  //   module: {
  //     rules: [
  //       {
  //         test: /\.?js(x)?$/,
  //         use: {
  //           loader: "babel-loader",
  //           options: {
  //             presets: ['@babel/preset-env', '@babel/preset-react']
  //           }
  //         },
  //       },
  //       {
  //         test: /\.css$/,
  //         use: [
  //           {
  //             loader: MiniCssExtractPlugin.loader,
  //             options: {
  //               hmr: debug,
  //             },
  //           },
  //           'css-loader',
  //         ],
  //       },
  //       {
  //         test: /\.(ttf|eot|svg|png|jpe?g|gif|ico)(\?.*)?$/i,
  //         loader: `file-loader?name=[path][name].[ext]`
  //       }
  //     ]
  //   }
  // },

  // {
  //   context: path.join(__dirname, '/edurange_refactored/templates/notification_history/components/'),
  //   entry: {
  //     Notification: './Notification',
  //   },
  //   output: {
  //     chunkFilename: "[id].js",
  //     filename: "[name].bundle.js",
  //     path: path.join(__dirname, "edurange_refactored", "static", "build"),
  //     publicPath: "/static/build/",
  //     library: "lib",
  //     libraryTarget: "var"


  //   },
  //   resolve: {
  //     extensions: [".js", ".jsx", ".css"]
  //   },
  //   plugins: [
  //     new MiniCssExtractPlugin({ filename: "[name].bundle.css" }),
  //   ],
  //   module: {
  //     rules: [
  //       {
  //         test: /\.?js(x)?$/,
  //         use: {
  //           loader: "babel-loader",
  //           options: {
  //             presets: ['@babel/preset-env', '@babel/preset-react']
  //           }
  //         },
  //       },
  //       {
  //         test: /\.css$/,
  //         use: [
  //           {
  //             loader: MiniCssExtractPlugin.loader,
  //             options: {
  //               hmr: debug,
  //             },
  //           },
  //           'css-loader',
  //         ],
  //       }
  //     ]
  //   }
  // },
  
  