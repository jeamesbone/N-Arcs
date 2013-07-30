part of narcMaker;

bool circleContainsPoint(Circle c, NarcPoint p) {
  num squareDist = pow(c.center.x - p.x, 2) + pow(c.center.y - p.y, 2);
  return squareDist < pow(c.radius, 2);
}

NarcPoint getPointBetween(NarcPoint p1, NarcPoint p2, [SvgElement svg]) {
  num x = p1.x - ((p1.x - p2.x) / 2);
  num y = p1.y - ((p1.y - p2.y) / 2);
  return new NarcPoint(x, y, svg);
}

num angleBetweenPoints(NarcPoint p1, NarcPoint p2) {
  if (p1.x - p2.x <= 1 && p1.y - p2.y <= 1) {
    return 0;
  }
  return acos((p2.x - p1.x) / distanceBetween(p1, p2));
}

num distanceBetween(NarcPoint a, NarcPoint b) {
  var dx = a.x - b.x;
  var dy = a.y - b.y;
  return sqrt(dx * dx + dy * dy);
}

NarcPoint rotatePointAroundPoint(NarcPoint point, NarcPoint anchor, num angle) {
  NarcPoint pointOrigin = new NarcPoint(point.x - anchor.x, point.y - anchor.y);
  NarcPoint tmp = new NarcPoint(0, 0);
  tmp.x = pointOrigin.x * cos(angle) - pointOrigin.y * sin(angle);
  tmp.y = pointOrigin.x * sin(angle) - pointOrigin.y * cos(angle);
  
  return new NarcPoint(tmp.x + anchor.x, tmp.y + anchor.y);
}

NarcPoint pointOnLine(NarcPoint start, NarcPoint end, NarcPoint pt)
{
  bool isValid = false;
  
  NarcPoint pt1 = rotatePointAroundPoint(start, getPointBetween(start, end), PI/2);
  NarcPoint pt2 = rotatePointAroundPoint(end, getPointBetween(start, end), PI/2);
  
  var r = new NarcPoint(0, 0);
  if (pt1.y == pt2.y && pt1.x == pt2.x) { pt1.y -= 0.00001; }

  var U = ((pt.y - pt1.y) * (pt2.y - pt1.y)) + ((pt.x - pt1.x) * (pt2.x - pt1.x));

  var Udenom = pow(pt2.y - pt1.y, 2) + pow(pt2.x - pt1.x, 2);

  U /= Udenom;

  r.y = pt1.y + (U * (pt2.y - pt1.y));
  r.x = pt1.x + (U * (pt2.x - pt1.x));
  
  return r;
}

class Narc {
  NarcPoint centroid;
  NarcPoint start;
  NarcPoint end;
  PathElement path;
  PathElement guideLines;
  
  Narc(this.start, this.end, [SvgElement svg]) {
    centroid = getPointBetween(start, end, svg);
    
    if (svg != null)
    {
      path = new PathElement();
      guideLines = new PathElement();
      drawArc();
      svg.append(path);
      svg.append(guideLines);
    }
  }
  
  void drawArc() {
    NarcPoint fixedCentroid = pointOnLine(start, end, centroid);
    centroid.x = fixedCentroid.x;
    centroid.y = fixedCentroid.y;    
    centroid.draw();
    int radius = distanceBetween(start, centroid).round();
    int sweepFlag = 0;
    int largeArcFlag = isLargeArc() ? 0 : 1;
    int rotation = 0;
    
    // Move to start position
    String pathString = "M" + start.x.toString() + "," + start.y.toString();
    // Radii
    pathString += " A" + radius.toString() + "," + radius.toString();
    // Flags
    pathString += " " + rotation.toString() + " " + largeArcFlag.toString() + " " + sweepFlag.toString() + " ";
    // End Point
    pathString += end.x.toString() + "," + end.y.toString();
    
    path.attributes['d'] =  pathString;
    path.attributes['stroke-width'] = 2.toString();
    path.attributes['stroke'] = "blue";
    path.attributes['fill'] = "none";
    
    String guideLinesString = "M" + start.x.toString() + "," + start.y.toString();
    guideLinesString += "L" + centroid.x.toString() + "," + centroid.y.toString();
    guideLinesString += " " + end.x.toString() + "," + end.y.toString();
    
    guideLines.attributes['d'] = guideLinesString;
    guideLines.attributes['stroke-width'] = 1.toString();
    guideLines.attributes['stroke'] = "gray";
    guideLines.attributes['fill'] = "none";
  }
  
  bool isLargeArc() {
    return ((end.x - start.x)*(centroid.y - start.y) - (end.y - start.y)*(centroid.x - start.x)) <= 0;
  }
}

class NarcPoint {
  num x;
  num y;
  Circle circle;
  
  NarcPoint(this.x, this.y, [SvgElement svg]) {
    circle = new Circle(this, 5, svg);
  }
  
  void draw() {
    circle.draw();
  }
}

class Circle {
  NarcPoint center;
  num radius;
  CircleElement element;
  
  Circle(this.center, this.radius, [SvgElement svg]) {
    if (svg != null) {
      element = new CircleElement();
      draw();
      svg.append(element);
    }
  }
  
  void draw() {
    if (element != null) {
      element.attributes['cx'] = center.x.toString();
      element.attributes['cy'] = center.y.toString();
      element.attributes['r'] = radius.toString();
      element.attributes['fill'] = "red";
    }
  }
}