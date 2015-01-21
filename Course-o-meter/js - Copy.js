function cbchange(checkbox,row)
{
	var row = document.getElementById(row);
	var cb = document.getElementById(checkbox);
	
	var temp,i,j,k,l,m,n;
	var totals = new Array(4);
	var totals2 = new Array(4);
	var finaltotals = new Array(4);
	var totals3;

	var hlcolor = "#FF9900";
	
	//highlight
	if (cb.checked) {row.bgColor = hlcolor ;
		}
	else {row.bgColor = "#ffffff";	
		}
	
	//total
	for (j=1;j<=4;j++){
		totals[j-1]=0;
		for (i=1;i<=10;i++) {
		
			if (document.getElementById("r" + i + "p" + j).innerHTML == "*" && document.getElementById("cb"+i).checked) {
			
			totals[j-1]++;
				
			}//if			
		}//for i
		document.getElementById("t"+j).innerHTML = totals[j-1];
	}//for j
	
	
	for (k=1;k<=4;k++){
		totals2[k-1]=0;
		for (l=11;l<=16;l++) {
		
			if (document.getElementById("r" + l + "p" + k).innerHTML == "*" && document.getElementById("cb"+l).checked) {
			
			totals2[k-1]++;
				
			}//if			
		}//for l
		temp = k+4;
		document.getElementById("t"+temp).innerHTML = totals2[k-1];
	}//for k
		
	totals3=0;
	for (m=17;m<=36;m++) {
		
		if ( document.getElementById("cb"+m).checked) {
			
			totals3++;
				
			}//if			
		
			
	}
	document.getElementById("t9").innerHTML = totals3;
	document.getElementById("t10").innerHTML = totals3;
	document.getElementById("t11").innerHTML = totals3;
	document.getElementById("t12").innerHTML = totals3;
	
	
	finaltotals[0]=totals[0]+totals2[0]+totals3;
		finaltotals[1]=totals[1]+totals2[1]+totals3;
			finaltotals[2]=totals[2]+totals2[2]+totals3;
				finaltotals[3]=totals[3]+totals2[3]+totals3;
	
	document.getElementById("endtotals").innerHTML = "Total: " + finaltotals ;
	
	
	
	
}//cbchange