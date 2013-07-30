library narcMaker;

import 'dart:html';
import 'dart:math';
import 'dart:svg';
import 'dart:async';

part 'geometry.dart';

List<NarcPoint> narcPoints;
List<Narc> narcs;

SvgSvgElement narcArea;

NarcPoint editing;
Narc editingCentroid;

void main() {
  // Initialize Data Arrays
  narcPoints = new List<NarcPoint>();
  narcs = new List<Narc>();
  
  // Set up event listeners on the designer area
  narcArea = query("#narcArea");
  narcArea.onMouseUp.listen(narcAreaUp);
  narcArea.onMouseMove.listen(narcAreaMoved);
  narcArea.onMouseDown.listen(narcAreaDown);
  
  // Scroll to the middle of the designer
  DivElement designerDiv = query("#designer");
  designerDiv.scrollLeft = 4600;
  designerDiv.scrollTop = 4700;
  
  // Set up event listeners on the buttons
  query("#reset")..onClick.listen(reset);
  query("#export")..onClick.listen(export);
}

void reset(MouseEvent e) {
  while (narcs.length > 0) {
    Narc oldNarc = narcs.removeLast();
    oldNarc.path.remove();
    oldNarc.guideLines.remove();
    oldNarc.centroid.circle.element.remove();
  }
  while (narcPoints.length > 0) {
    removePoint(narcPoints[0]);
  }
}

void export(MouseEvent e) {
  DivElement exportBack = query("#exportPopupBack");
  exportBack.style.display = "block";
  
  DivElement export = query("#exportPopup");
  export.style.display = "block";
  export.innerHtml = getData();
  
  ButtonElement closeButton = new ButtonElement();
  closeButton.innerHtml = "Close";
  closeButton.onClick.listen(exportClose);
  export.append(closeButton);
}

void exportClose(MouseEvent e) {
  DivElement exportBack = query("#exportPopupBack");
  exportBack.style.display = "none";
  
  DivElement export = query("#exportPopup");
  export.style.display = "none";
}

String getData() {
  String data = "<h2> Exported Narcs in .csv format </h2> <br /> <br />"; 
  data += "id, startx, starty, endx, endy, centroidx, centroidy <br />";
  for (Narc n in narcs) {
    data += narcs.indexOf(n).toString() + ",";
    data += n.start.x.toString() + "," + n.start.y.toString() + ",";
    data += n.end.x.toString() + "," + n.end.y.toString() + ",";
    data += n.centroid.x.toString() + "," + n.centroid.y.toString() + "<br />";
  }
  data += "<br /> <br />";
  return data;
}

void narcAreaDown(MouseEvent e) {
  if (editing != null) {
    return;
  }
  
  NarcPoint touchPoint = new NarcPoint(e.offset.x, e.offset.y);
  for (NarcPoint p in narcPoints) {
    if (circleContainsPoint(p.circle, touchPoint)) {
      editingCentroid = null;
      editing = p;
    }
  }
  
  for (Narc n in narcs) {
    if (circleContainsPoint(n.centroid.circle, touchPoint)) {
      editingCentroid = n;
      editing = null;
    }
  }
}

void narcAreaMoved(MouseEvent e) {
  if (editing != null) {
    NarcPoint touchPoint = new NarcPoint(e.offset.x, e.offset.y);
    editing.x = touchPoint.x;
    editing.y = touchPoint.y;
    reDrawPoints();
    reDrawArcs();
  }
  else if (editingCentroid != null) {
    NarcPoint touchPoint = new NarcPoint(e.offset.x, e.offset.y);
    NarcPoint fixedTouchPoint = pointOnLine(editingCentroid.start, editingCentroid.end, touchPoint);
    editingCentroid.centroid.x = fixedTouchPoint.x;
    editingCentroid.centroid.y = fixedTouchPoint.y;    
    reDrawPoints();
    reDrawArcs();
  }
}

void narcAreaUp(MouseEvent e) {
  NarcPoint touchPoint = new NarcPoint(e.offset.x, e.offset.y);
  
  if (editing != null) {
    editing = null;
    return;
  }
  if (editingCentroid != null) {
    editingCentroid = null;
    return;
  }
  
  for (NarcPoint p in narcPoints)
  {
    if (circleContainsPoint(p.circle, touchPoint)) {
      removePoint(p);
      generateArcs();
      return;
    }
  }
  
  narcPoints.add(new NarcPoint(e.offset.x, e.offset.y, narcArea));
  generateArcs();
}

void reDrawArcs() {
  for (Narc n in narcs) {
    n.drawArc();
  }
}

void reDrawPoints() {
  for (NarcPoint p in narcPoints) {
    p.draw();
  }
}

void generateArcs() {
  while (narcs.length > 0) {
    Narc oldNarc = narcs.removeLast();
    oldNarc.path.remove();
    oldNarc.guideLines.remove();
    oldNarc.centroid.circle.element.remove();
  }
  
  if (narcPoints.length > 2) {
    for(int i = 0; i < narcPoints.length; i++) {
      narcs.add(new Narc(narcPoints[i], narcPoints[(i + 1) % narcPoints.length], narcArea));
    }
  }
}

void removePoint(NarcPoint p)
{
  p.circle.element.remove();
  narcPoints.remove(p);
}