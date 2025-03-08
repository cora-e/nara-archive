
import  * as fs         from "fs";
import  * as JSONStream from "JSONStream";
import  * as es         from "event-stream";

fs.createReadStream('../record_format.txt')
  .pipe(JSONStream.parse('*.record'))
    // If this record is "relevant", pass it on.
    .pipe(es.mapSync((r)=>{
      const allDescriptionText = [
        ...r?.ancestors?.map((a)=>([a.title||'',...(a.creators||[]).map((c)=>(c.heading||''))])),
        r?.dataControlGroup?.groupName ||'',
        r?.scopeAndContentNote         ||'',
        r?.title                       ||'',
      ].join(" ");
      // If any regex phrase of interest is found, send the record on.
      if (/\b(grading|planting) plan\b/i.test(allDescriptionText)) {
        return r;
      }
      // ...
    }))
    // If this record has digital objects, send on the URLs.
    .pipe(es.mapSync((r)=>{
      if (r?.digitalObjects?.length) {
        return r.digitalObjects.map((o)=>(o.objectUrl));
      }
    }))
    // List of relevant URLs, get their contents.
    .pipe(es.mapSync((a)=>{
      for (const url of a) {
        console.log('Get the contents of: ',url);
      }
    }));
