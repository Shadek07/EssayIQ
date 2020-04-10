'use strict';

/**
 * @ngdoc overview
 * @name conceptvectorApp
 * @description
 * # conceptvectorApp
 *
 * Main module of the application.
 */
angular
  .module('conceptvectorApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch',
    'ui.bootstrap',
    'ngTagsInput',
    'nvd3',
    'angularUtils.directives.dirPagination',
    'ui.select',
    'cgBusy',
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl',
        controllerAs: 'main',
        access: {restricted: false}
      })
      .when('/about', {
        templateUrl: 'views/about.html',
        controller: 'AboutCtrl',
        controllerAs: 'about',
        access: {restricted: false}
      })
      .when('/login', {
        templateUrl: 'views/login.html',
        controller: 'LoginCtrl',
        access: {restricted: false}
      })
      .when('/logout', {
        templateUrl: 'views/logout.html',
        controller: 'LogoutCtrl',
        access: {restricted: true}
      })
      .when('/register', {
        templateUrl: 'views/register.html',
        controller: 'RegisterCtrl',
        access: {restricted: false}
      })
      .when('/assignments', {
        templateUrl: 'views/assignmentlist.html',
        controller: 'AssignmentlistCtrl',
        access: {restricted: true}
      })
      .when('/assignments/:assignmentId',{
        templateUrl: 'views/customassignment.html',
        controller: 'AssignmentdetailCtrl'
      })
      .when('/submissions', {
        templateUrl: 'views/submissionlist.html',
        controller: 'SubmissionlistCtrl',
        access: {restricted: false}
      })
      .when('/submissions/:submissionId',{
        templateUrl: 'views/submissionpage.html',
        controller: 'submissionpageCtrl'
      })
      .when('/wholesubmissions/:assignmentID',{
        templateUrl: 'views/analyzewholesubmissions.html',
        controller: 'analyzewholesubmissionsCtrl'
      })
      .when('/annotatewholesubmissions/:assignmentID',{
        templateUrl: 'views/annotatewholesubmissions.html',
        controller: 'annotatewholesubmissionsCtrl'
      })
      .when('/submissions/:submissionID/:assignmentID',{
        templateUrl: 'views/analyzesubmission.html',
        controller: 'analyzesubmissionCtrl'
      })
      .when('/themes', {
        templateUrl: 'views/themelist.html',
        controller: 'themelistCtrl',
        access: {restricted: true}
      })
      .when('/themes/:themeId',{
        templateUrl: 'views/themeadd.html',
        controller: 'themeAddCtrl'
      })
      .when('/concepts', {
        templateUrl: 'views/conceptlist.html',
        controller: 'ConceptlistCtrl',
        access: {restricted: false}
      })
      .when('/concepts/:conceptId', {
        templateUrl: 'views/customconcept.html',
        controller: 'ConceptdetailCtrl',
      })
      .when('/articles/:articleId', {
        templateUrl: 'views/commentdemo.html',
        controller: 'CommentdemoCtrl',
      })
      .when('/articles', {
        templateUrl: 'views/articles.html',
        controller: 'ArticlesCtrl'
      })
      .when('/twitter', {
        templateUrl: 'views/twitter.html',
        controller: 'TwitterCtrl',
        controllerAs: 'twitter'
      })
      .otherwise({
        redirectTo: '/'
      });
  }).run(function ($rootScope, $location, $route, AuthService) {
  $rootScope.$on('$routeChangeStart', function (event, next, current) {
    AuthService.getUserStatus();

    if (!next.access) {
      return;
    }
    if (next.access.restricted && (AuthService.isLoggedIn() === false)) {
      $location.path('/login');
      $route.reload();
    }
  });
});

/*
.when('/themes_filterbyassignment/:assignment_id',{
        templateUrl: 'views/themeadd.html',
        controller: 'themeAddCtrl'
      })
*/
