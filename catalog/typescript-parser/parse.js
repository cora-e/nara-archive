"use strict";
var __spreadArray = (this && this.__spreadArray) || function (to, from, pack) {
    if (pack || arguments.length === 2) for (var i = 0, l = from.length, ar; i < l; i++) {
        if (ar || !(i in from)) {
            if (!ar) ar = Array.prototype.slice.call(from, 0, i);
            ar[i] = from[i];
        }
    }
    return to.concat(ar || Array.prototype.slice.call(from));
};
exports.__esModule = true;
var fs = require("fs");
var JSONStream = require("JSONStream");
var es = require("event-stream");
fs.createReadStream('../record_format.txt')
    .pipe(JSONStream.parse('*.record'))
    // If this record is "relevant", pass it on.
    .pipe(es.mapSync(function (r) {
    var _a, _b;
    var allDescriptionText = __spreadArray(__spreadArray([], (_a = r === null || r === void 0 ? void 0 : r.ancestors) === null || _a === void 0 ? void 0 : _a.map(function (a) { return (__spreadArray([a.title || ''], (a.creators || []).map(function (c) { return (c.heading || ''); }), true)); }), true), [
        ((_b = r === null || r === void 0 ? void 0 : r.dataControlGroup) === null || _b === void 0 ? void 0 : _b.groupName) || '',
        (r === null || r === void 0 ? void 0 : r.scopeAndContentNote) || '',
        (r === null || r === void 0 ? void 0 : r.title) || '',
    ], false).join(" ");
    // If any regex phrase of interest is found, send the record on.
    if (/\b(grading|planting) plan\b/i.test(allDescriptionText)) {
        return r;
    }
    // ...
}))
    // If this record has digital objects, send on the URLs.
    .pipe(es.mapSync(function (r) {
    var _a;
    if ((_a = r === null || r === void 0 ? void 0 : r.digitalObjects) === null || _a === void 0 ? void 0 : _a.length) {
        return r.digitalObjects.map(function (o) { return (o.objectUrl); });
    }
}))
    // List of relevant URLs, get their contents.
    .pipe(es.mapSync(function (a) {
    for (var _i = 0, a_1 = a; _i < a_1.length; _i++) {
        var url = a_1[_i];
        console.log('Get the contents of: ', url);
    }
}));
