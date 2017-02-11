module.exports = function(grunt) {
  require('load-grunt-tasks')(grunt);

  var config = grunt.file.readYAML('Gruntconfig.yml');

  grunt.initConfig({
    sass: {
      dist: {
        src: config.sassDir + 'style.scss',
        dest: config.cssDir + 'style.css'
      }
    },
    concat: {
      dist: {
        src: config.jsSrcDir + '*.js',
        dest: config.jsConcatDir + 'app.js'
      }
    },
    jshint: {
      all: [
        'Gruntfile.js',
        config.jsSrcDir + '*.js'
      ]
    }
  });

  grunt.registerTask('default', [
    'jshint',
    'sass',
    'concat'
  ]);
};
