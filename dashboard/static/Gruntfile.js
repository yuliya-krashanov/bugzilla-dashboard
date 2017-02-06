module.exports = function (grunt) {
    grunt.initConfig({
        sass: {
            dist: {
                options: {
                    compress: false
                },
                files: {
                    "public/css/all.css": "assets/stylesheets/all.scss"
                }
            }
        },
        browserify: {
			dist: {
				files: {
					'public/js/app.js': ['assets/javascripts/App.jsx']
				},
				options: {
					transform: [
						['babelify', {presets: ['es2015', 'react']}]
					]
				}
			}
		},
        postcss: {
            options: {
                map: true,
                processors: [
                   require('autoprefixer')
                ]
            },
            dist: {
                src: 'public/css/*.css'
            }
        },
        copy: {
            dist: {
                files: [
                  // includes files within path and its sub-directories
                  {
                      expand: true,
                      cwd: 'node_modules/bootstrap-sass/assets/fonts/',
                      src: '**',
                      dest: 'public/fonts/'
                  },
                  {
                      expand: true,
                      cwd: 'assets/fonts/',
                      src: '**',
                      dest: 'public/fonts/'
                  }
                ],
            },
        },
        clean: ['public/**'],
		watch: {
			js: {
				files: ['assets/javascripts/**/*.js', 'assets/javascripts/**/*.jsx'],
				tasks: ['browserify']
			},
            scss: {
				files: ['assets/stylesheets/**/*.scss'],
				tasks: ['sass']
			}
		}
    });

    // Plugin loading

    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-browserify');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-postcss');


	grunt.registerTask('build', ['clean', 'browserify', 'copy', 'sass', 'postcss']);
	grunt.registerTask('default', ['clean', 'browserify', 'copy', 'sass', 'postcss', 'watch']);
};