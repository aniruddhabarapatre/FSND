module.exports = function(grunt) {
  grunt.loadNpmTasks('grunt-sass');

  grunt.initConfig({
    sass: {
      dist: {
        src: 'src/sass/style.scss',
        dest: 'dist/css/style.css'
      }
    }
  });

  grunt.registerTask('default', [
    'sass'
  ]);
}
